from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os


class SparkPostgresLoader:
    def __init__(self):
        load_dotenv(override=True)
        self.app_name = os.getenv("APP_NAME")
        self.postgres_v = os.getenv("POSTGRES_VERSION")
        self.postgres_url = os.getenv("POSTGRES_URL")
        self.postgres_user = os.getenv("POSTGRES_USER")
        self.postgres_pass = os.getenv("POSTGRES_PASSWORD")
        self.postgres_table = os.getenv("POSTGRES_TABLE")
        self.output_path = os.getenv("OUTPUT_PATH")
        self.spark = None
        self.dataframe_ = None

    def initialize_spark(self):
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .config("spark.jars.packages", self.postgres_v) \
            .getOrCreate()

    def load_parquet(self):
        if self.spark is None:
            raise Exception("Spark session not initialized. Call initialize_spark() first.")
        self.dataframe_ = self.spark.read.parquet(self.output_path)
        return self.dataframe_

    def print_schema_and_count(self):
        self.dataframe_.printSchema()
        print(self.dataframe_.count())

    def write_to_postgres(self):
        postgresql_properties = {
            "user": self.postgres_user,
            "password": self.postgres_pass,
            "driver": "org.postgresql.Driver"
        }
        self.dataframe_.write \
            .jdbc(self.postgres_url, self.postgres_table, mode="overwrite", properties=postgresql_properties)
        print("Data loaded to PostgresSQL successfully")

    def close_spark(self):
        if self.spark is not None:
            self.spark.stop()


def read_parquet_and_write_to_postgres():
    loader = SparkPostgresLoader()
    loader.initialize_spark()
    df = loader.load_parquet()
    loader.print_schema_and_count()
    loader.write_to_postgres()
    loader.close_spark()


if __name__ == "__main__":
    read_parquet_and_write_to_postgres()
