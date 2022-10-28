from .interfaces import (
    Engine,
    IsNumericChecker,
    IsCategoricalChecker,
    IsIdChecker,
    IsDateChecker,
    IsCharChecker,
)


class Table:
    def __init__(self, engine: Engine):
        self.engine: Engine = engine

    def num(self, column_name: str) -> IsNumericChecker:
        return self.engine.num(column_name)

    def cat(self, column_name: str) -> IsCategoricalChecker:
        return self.engine.cat(column_name)

    def id(self, column_name: str) -> IsIdChecker:
        return self.engine.id(column_name)

    def date(self, column_name: str) -> IsDateChecker:
        return self.engine.date(column_name)

    def char(self, column_name: str) -> IsCharChecker:
        return self.engine.char(column_name)

    def _run(self):
        tests = self.engine.get_tests()
        results = [t() for t in tests]
        for r in results:
            if not r.has_test_passed():
                print(r.get_message())
            else:
                print("All Green!")
        self.engine.destroy()
