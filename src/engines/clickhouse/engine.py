from .driver import Driver
from ...interfaces import (
    IsNumericChecker,
    IsCategoricalChecker,
    IsIdChecker,
    IsCharChecker,
    IsDateChecker,
    Checker,
    Test,
)


class ClickhouseEngine:
    def __init__(self, driver: Driver):
        self.driver: Driver = driver
        self.checkers: list[Checker] = []

    def num(self, table_name: str, column_name: str) -> IsNumericChecker:
        pass

    def cat(self, table_name: str, column_name: str) -> IsCategoricalChecker:
        pass

    def id(self, table_name: str, column_name: str) -> IsIdChecker:
        pass

    def date(self, table_name: str, column_name: str) -> IsDateChecker:
        pass

    def char(self, table_name: str, column_name: str) -> IsCharChecker:
        pass

    def get_tests(self) -> list[Test]:
        pass

    def destroy(self):
        pass
