from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# Initialize Spark session with Kafka dependencies and PostgreSQL driver
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.1,org.postgresql:postgresql:42.2.20") \
    .getOrCreate()

# Define schema for incoming data
schema = StructType([
    StructField("price", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("event_time", StringType(), True)
])

# Read data from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "crypto-prices") \
    .load()

# Parse the value field
value_df = df.selectExpr("CAST(value AS STRING)")

# Convert JSON string to DataFrame
json_df = value_df.select(from_json(col("value"), schema).alias("data")).select("data.*")

# Convert event_time to timestamp
json_df = json_df.withColumn("event_time", to_timestamp(col("event_time")))

# Define PostgreSQL connection properties
postgresql_url = "jdbc:postgresql://localhost:5432/postgres"
postgresql_properties = {
    "user": "postgres",
    "password": "admin",
    "driver": "org.postgresql.Driver"
}

# Write stream to PostgreSQL
query = json_df.select("price", "symbol", "event_time") \
    .writeStream \
    .outputMode("append") \
    .format("jdbc") \
    .option("url", postgresql_url) \
    .option("dbtable", "crypto_prices") \
    .option("user", postgresql_properties["user"]) \
    .option("password", postgresql_properties["password"]) \
    .option("driver", postgresql_properties["driver"]) \
    .start()

query.awaitTermination()
