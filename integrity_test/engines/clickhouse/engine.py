from integrity_test.test_result import TestResult
from .numeric import ClickHouseNumericColumn
from .driver import Driver
from ...protocols import (
    IsCategoricalColumn,
    IsIdColumn,
    IsCharColumn,
    IsDateColumn,
    Column,
)

ClickhouseChecker = Column[Driver]


class ClickhouseEngine:
    def __init__(self, driver: Driver):
        self.driver: Driver = driver
        self.checkers: list[ClickhouseChecker] = []

    def num(self, table_name: str, column_name: str) -> ClickHouseNumericColumn:
        checker = ClickHouseNumericColumn(table_name, column_name)
        self.checkers.append(checker)
        return checker

    def cat(self, table_name: str, column_name: str) -> IsCategoricalColumn:
        pass

    def id(self, table_name: str, column_name: str) -> IsIdColumn:
        pass

    def date(self, table_name: str, column_name: str) -> IsDateColumn:
        pass

    def char(self, table_name: str, column_name: str) -> IsCharColumn:
        pass

    def run_tests(self) -> list[TestResult]:
        print(self.checkers[0].get_tests())
        return [
            t(self.driver) for checker in self.checkers for t in checker.get_tests()
        ]

    def __del__(self):
        pass
