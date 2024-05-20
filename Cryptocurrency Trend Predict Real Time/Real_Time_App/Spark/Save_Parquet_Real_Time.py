from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, TimestampType
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Load environment variables
postgres_v = os.getenv("POSTGRES_VERSION")
kafka_v = os.getenv("KAFKA_VERSION")
config_ = f"{kafka_v},{postgres_v}"
kafka_server = os.getenv("KAFKA_SERVER")
kafka_topic = os.getenv("KAFKA_TOPIC")
column_1_name = os.getenv("COLUMN_1")
column_2_name = os.getenv("COLUMN_2")
column_3_name = os.getenv("COLUMN_3")
format_file = os.getenv("FORMAT_FILE")
output_path = os.getenv("OUTPUT_PATH")
checkpoint_location = os.getenv("CHECKPOINT_LOCATION")

# Initialize Spark session with Kafka dependencies and PostgreSQL driver
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", config_) \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField(column_1_name, StringType(), True),
    StructField(column_2_name, StringType(), True),
    StructField(column_3_name, StringType(), True)
])

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_server) \
    .option("subscribe", kafka_topic) \
    .load()

# Parse the value field
value_df = df.selectExpr("CAST(value AS STRING)")

# Convert JSON string to DataFrame
json_df = value_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Convert event_time to timestamp
json_df = json_df.withColumn(column_3_name, to_timestamp(col(column_3_name)))

# Write stream to Parquet files
query = json_df.writeStream \
    .outputMode("append") \
    .format(format_file) \
    .option("path", output_path) \
    .option("checkpointLocation", checkpoint_location) \
    .start()

query.awaitTermination()
