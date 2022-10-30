from abc import ABC
from .test_factories.protocols import ClickHouseTest


class ClickHouseColumn(ABC):
    def __init__(self, table_name: str, column_name: str):
        self._table_name = table_name
        self._column_name = column_name
        self._tests: list[ClickHouseTest] = []

    def get_tests(self):
        return self._tests
