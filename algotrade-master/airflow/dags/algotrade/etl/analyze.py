from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import FloatType
from loguru import logger

from statsforecast.distributed.utils import forecast
from statsforecast.distributed.fugue import FugueBackend
from statsforecast.models import AutoARIMA

from src.core.config import SPARK_CONFIG, NODES


spark = SparkSession \
    .builder \
    .master(f'{SPARK_CONFIG.DRIVER}://{SPARK_CONFIG.HOST}:{SPARK_CONFIG.PORT}') \
    .appName('algotrade-predictions-analyze') \
    .getOrCreate()

query = 'SELECT id, secid, begin, close from default.candles ORDER BY begin DESC'
dataframe = spark.read.format("jdbc") \
    .option('driver', 'com.github.housepower.jdbc.ClickHouseDriver') \
    .option('url', f'jdbc:clickhouse://{NODES[0].HOST}:{NODES[0].PORT}') \
    .option('user', NODES[0].USER) \
    .option('password',  NODES[0].PASSWORD) \
    .option('query', query) \
    .load()

print(dataframe.show(10, False))
logger.info(dataframe.count())

df = dataframe.select(
    col("secid").alias('unique_id'),
    dataframe.begin.alias('ds'),
    dataframe.close.astype(FloatType()).alias('y')
)

backend = FugueBackend(spark, {"fugue.spark.use_pandas_udf":True})
result_df = forecast(
    df,
    models=[AutoARIMA()],
    freq='H',
    h=1,
    parallel=backend
)

print(result_df.show(10, False))

result_df.write \
    .format("jdbc") \
    .mode("append") \
    .option('driver', 'com.github.housepower.jdbc.ClickHouseDriver') \
    .option('url', f'jdbc:clickhouse://{NODES[0].HOST}:{NODES[0].PORT}') \
    .option('user', NODES[0].USER) \
    .option('password',  NODES[0].PASSWORD) \
    .option("dbtable", "default.predictions") \
    .option("batchsize", 100000) \
    .option("isolationLevel", "NONE") \
    .save()

logger.info('[+] Success analyzing')