from .interfaces import (
    Engine,
    IsNumericChecker,
    IsCategoricalChecker,
    IsIdChecker,
    IsDateChecker,
    IsCharChecker,
)


class Table:
    def __init__(self, engine: Engine, table_name: str):
        self._engine: Engine = engine
        self._table_name: str = table_name

    def num(self, column_name: str) -> IsNumericChecker:
        return self._engine.num(self._table_name, column_name)

    def cat(self, column_name: str) -> IsCategoricalChecker:
        return self._engine.cat(self._table_name, column_name)

    def id(self, column_name: str) -> IsIdChecker:
        return self._engine.id(self._table_name, column_name)

    def date(self, column_name: str) -> IsDateChecker:
        return self._engine.date(self._table_name, column_name)

    def char(self, column_name: str) -> IsCharChecker:
        return self._engine.char(self._table_name, column_name)

    def run(self):
        tests = self._engine.get_tests()
        results = [t() for t in tests]
        for r in results:
            if not r.has_test_passed():
                print(r.get_message())
            else:
                print("All Green!")
        self._engine.destroy()
