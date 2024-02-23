from pyspark.sql.types import StructType, StructField, StringType, TimestampType, FloatType


PREDICTION = StructType(fields=[
    StructField(name='secid', dataType=StringType(), nullable=False),
    StructField(name='algorithm', dataType=StringType(), nullable=False),
    StructField(name='value', dataType=FloatType(), nullable=True),
    StructField(name='timestamp', dataType=TimestampType(), nullable=False),
])
