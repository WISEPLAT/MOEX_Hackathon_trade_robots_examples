from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType, IntegerType


CANDLE = StructType(fields=[
    StructField(name='id', dataType=StringType(), nullable=False),
    StructField(name='secid', dataType=StringType(), nullable=False),
    StructField(name='open', dataType=FloatType(), nullable=True),
    StructField(name='close', dataType=FloatType(), nullable=True),
    StructField(name='high', dataType=FloatType(), nullable=True),
    StructField(name='low', dataType=FloatType(), nullable=True),
    StructField(name='value', dataType=FloatType(), nullable=True),
    StructField(name='volume', dataType=IntegerType(), nullable=True),
    StructField(name='begin', dataType=TimestampType(), nullable=False),
    StructField(name='end', dataType=TimestampType(), nullable=False),
])
