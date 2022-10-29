from typing import Callable
from .driver import Driver
from ...test_result import TestResult
from .test_factories import missing, in_range
from ...null import NullType

ClickhouseTest = Callable[[Driver], TestResult]


class NotClickHouseNumericColumn:
    def __init__(self, table_name: str, column_name: str):
        self._table_name = table_name
        self._column_name = column_name
        self._tests: list[ClickhouseTest] = []

    def missing(self, missing_value: int | str | NullType):
        factory = missing.NotMissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def in_range(
        self,
        value_range: tuple[int | float, int | float],
        missing_value: int | str | NullType | None = None,
    ):
        factory = in_range.NotInRangeNumericFactory()
        value_min, value_max = value_range
        test = factory.make_test(
            self._table_name, self._column_name, value_min, value_max, missing_value
        )
        self._tests.append(test)

    def get_tests(self):
        return self._tests


class ClickHouseNumericColumn:
    def __init__(self, table_name: str, column_name: str):
        self._table_name = table_name
        self._column_name = column_name
        self._tests: list[ClickhouseTest] = []
        self.n = NotClickHouseNumericColumn(table_name, column_name)

    def missing(self, missing_value: int | str | NullType):
        factory = missing.MissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def in_range(
        self,
        value_range: tuple[int | float, int | float],
        missing_value: int | str | NullType | None = None,
    ):
        factory = in_range.InRangeNumericFactory()
        value_min, value_max = value_range
        test = factory.make_test(
            self._table_name, self._column_name, value_min, value_max, missing_value
        )
        self._tests.append(test)

    def get_tests(self):
        return self._tests + self.n.get_tests()
