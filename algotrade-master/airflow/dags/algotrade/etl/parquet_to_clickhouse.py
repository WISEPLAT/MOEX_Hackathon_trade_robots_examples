from redis import Redis
from pyspark.sql import SparkSession
from loguru import logger

from src.core.config import NODES, HDFS_CONFIG, SPARK_CONFIG, REDIS_CONFIG
from src.transform.prediction import PredictionTransformer
from src.load.clickhouse import ClickhouseLoader
from src.state.redis import RedisState
from src.schemas.prediction import PREDICTION


spark = SparkSession \
    .builder \
    .master(f'{SPARK_CONFIG.DRIVER}://{SPARK_CONFIG.HOST}:{SPARK_CONFIG.PORT}') \
    .appName('algotrade-predictions-load_to_clickhouse') \
    .getOrCreate()

dataframe = spark.read.schema(PREDICTION).parquet(
    f'{HDFS_CONFIG.DRIVER}://{HDFS_CONFIG.HOST}:{HDFS_CONFIG.PORT}/{HDFS_CONFIG.PATH}/algotrade-predictions'
)

redis = Redis(
    host=REDIS_CONFIG.HOST, port=REDIS_CONFIG.PORT, password=REDIS_CONFIG.PASSWORD
)
state = RedisState(redis=redis)

logger.info('[*] Loading predictions to clickhouse')

result_transformer = PredictionTransformer()
loader = ClickhouseLoader(
    host=NODES[2].HOST,
    port=NODES[2].PORT,
    user=NODES[2].USER,
    password=NODES[2].PASSWORD,
    alt_hosts=[f"{NODE.HOST}:{NODE.PORT}" for NODE in NODES],
    state=state,
)

result_data = result_transformer.transform(
    (elem.asDict() for elem in dataframe.rdd.toLocalIterator()),
    to_dict=True
)

result = loader.load(data=result_data, table='predictions')
logger.info(result)

logger.info('[+] Success loading predictions to clickhouse')