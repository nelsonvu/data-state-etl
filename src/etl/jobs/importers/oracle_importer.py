import collections

from etl.jobs.exporters.converters.composite_item_converter import CompositeItemConverter
from etl.jobs.importers.base_importer import BaseImporter

class OracleImporter(BaseImporter):

    def __init__(self, 
        oracle_url,
        oracle_user,
        oracle_password, 
        converters=(), 
        print_sql=True
    ):
        self.oracle_url = oracle_url
        self.oracle_user = oracle_user
        self.oracle_password = oracle_password
        self.converter = CompositeItemConverter(converters)

        self.engine = self.create_engine()

    def open(self):
        pass

    def import_items(self, queries):
        pass

    def import_item(self, query):
        user = "username"
        password = "userpassword"
        # Change this to your Oracle's details accordingly
        jdbcDriver = "oracle.jdbc.driver.OracleDriver"


    def convert_items(self, items):
        for item in items:
            yield self.converter.convert_item(item)

    def create_engine(self):
        pass

    def close(self):
        pass
