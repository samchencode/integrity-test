from integrity_test.test_result import TestResult
from .protocols import (
    Engine,
    IsNumericColumn,
    IsCategoricalColumn,
    IsIdColumn,
    IsDateColumn,
    IsCharColumn,
)


class Table:
    def __init__(self, engine: Engine, table_name: str):
        self._engine: Engine = engine
        self._table_name: str = table_name

    def num(self, column_name: str) -> IsNumericColumn:
        return self._engine.num(self._table_name, column_name)

    def cat(self, column_name: str) -> IsCategoricalColumn:
        return self._engine.cat(self._table_name, column_name)

    def id(self, column_name: str) -> IsIdColumn:
        return self._engine.id(self._table_name, column_name)

    def date(self, column_name: str) -> IsDateColumn:
        return self._engine.date(self._table_name, column_name)

    def char(self, column_name: str) -> IsCharColumn:
        return self._engine.char(self._table_name, column_name)

    def run_tests(self) -> list[TestResult]:
        return self._engine.run_tests()

    def get_name(self):
        return self._table_name
