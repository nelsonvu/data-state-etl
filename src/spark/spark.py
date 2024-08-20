from pyspark.sql import SparkSession

class Spark:
    def __init__(self, master, app_name):
        self.master = master
        self.app_name = app_name

        self.create_engine()

    def create_engine(self):
        # Create Spark session
        self.spark_session = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .getOrCreate()