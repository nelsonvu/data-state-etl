from abc import abstractmethod
from typing import List


class BaseImporter(object):
    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def import_items(self, queries: List[str]):
        pass

    @abstractmethod
    def import_item(self, query: str):
        pass

    @abstractmethod
    def convert_items(self, items):
        pass

    @abstractmethod
    def close(self):
        pass

