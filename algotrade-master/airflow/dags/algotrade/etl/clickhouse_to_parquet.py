from pyspark.sql import SparkSession
from loguru import logger

from src.core.config import NODES, HDFS_CONFIG, SPARK_CONFIG
from src.extract.clickhouse import ClickhouseExtractor
from src.transform.candle import CandleTSTransformer
from src.schemas.candle import CANDLE


spark = SparkSession \
    .builder \
    .master(f'{SPARK_CONFIG.DRIVER}://{SPARK_CONFIG.HOST}:{SPARK_CONFIG.PORT}') \
    .appName('algotrade-candle-clickhouse_to_parquet') \
    .getOrCreate()

spark_context = spark.sparkContext

logger.info('[*] Starting etl process clickhouse to spark')

extractor = ClickhouseExtractor(
    host=NODES[0].HOST,
    port=NODES[0].PORT,
    user=NODES[0].USER,
    password=NODES[0].PASSWORD,
    alt_hosts=[f'{NODE.HOST}:{NODE.PORT}' for NODE in  NODES[1:]],
    settings={'use_numpy': True}
)
transformer = CandleTSTransformer()

query = 'SELECT * FROM default.candles ORDER BY begin DESC'
raw_data = extractor.extract(query=query)
data = transformer.transform(raw_data, to_dict=True)

rdd = spark_context.parallelize(data)
dataframe = spark.createDataFrame(rdd, CANDLE)

logger.info(dataframe.show(10, False))
logger.info(dataframe.count())
logger.info(dataframe.printSchema())

dataframe.write.parquet(
    path=f'{HDFS_CONFIG.DRIVER}://{HDFS_CONFIG.HOST}:{HDFS_CONFIG.PORT}/{HDFS_CONFIG.PATH}/algotrade-candle-clickhouse-to-parquet',
    mode='overwrite'
)

logger.info('[+] Success finished etl process clickhouse to spark')
