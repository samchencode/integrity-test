from .categorical import ClickHouseCategoricalColumn
from .date import ClickHouseDateColumn
from ...test_result import TestResult
from .numeric import ClickHouseNumericColumn
from .driver import Driver
from ...protocols import (
    IsCategoricalColumn,
    IsIdColumn,
    IsCharColumn,
    IsDateColumn,
    Column,
    IsNumericColumn,
)

ClickHouseChecker = Column[Driver]


class ClickHouseEngine:
    def __init__(self, driver: Driver):
        self.driver: Driver = driver
        self.columns: list[ClickHouseChecker] = []

    def num(self, table_name: str, column_name: str) -> IsNumericColumn:
        column = ClickHouseNumericColumn(table_name, column_name)
        self.columns.append(column)
        return column

    def cat(self, table_name: str, column_name: str) -> IsCategoricalColumn:
        column = ClickHouseCategoricalColumn(table_name, column_name)
        self.columns.append(column)
        return column

    def id(self, table_name: str, column_name: str) -> IsIdColumn:
        pass

    def date(self, table_name: str, column_name: str) -> IsDateColumn:
        column = ClickHouseDateColumn(table_name, column_name)
        self.columns.append(column)
        return column

    def char(self, table_name: str, column_name: str) -> IsCharColumn:
        pass

    def run_tests(self) -> list[TestResult]:
        print(self.columns[0].get_tests())
        return [t(self.driver) for checker in self.columns for t in checker.get_tests()]

    def __del__(self):
        pass
