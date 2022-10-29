from typing import Protocol, Callable, Generic, TypeVar
from .test_result import TestResult

T = TypeVar("T")

Test = Callable[[T], TestResult]


class Checker(Protocol, Generic[T]):
    def get_tests(self) -> list[Test[T]]:
        ...


class NumericChecker(Checker, Protocol):
    def missing(self, missing_value: int | str):
        ...

    def in_range(
        self, value_range: tuple[int | float, int | float], missing_value: int | str
    ):
        ...


class NotNumericChecker(NumericChecker, Protocol):
    ...


class IsNumericChecker(NumericChecker, Protocol):
    n: NotNumericChecker


class DateChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def in_range(self, value_range: tuple[str, str], missing_value: str):
        ...


class NotDateChecker(DateChecker, Protocol):
    ...


class IsDateChecker(DateChecker, Protocol):
    n: NotDateChecker


class CategoricalChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def one_of(self, values: list[str]):
        ...


class NotCategoricalChecker(CategoricalChecker, Protocol):
    ...


class IsCategoricalChecker(CategoricalChecker, Protocol):
    n: NotCategoricalChecker


class IdChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def unique(self):
        ...

    def in_reference_to(self, table_name: str, column_name: str):
        ...


class NotIdChecker(IdChecker, Protocol):
    ...


class IsIdChecker(IdChecker, Protocol):
    n: NotIdChecker


class CharChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def match(self, pattern=str):
        ...


class NotCharChecker(CharChecker, Protocol):
    ...


class IsCharChecker(CharChecker, Protocol):
    n: NotCharChecker


class Engine(Protocol):
    def num(self, table_name: str, column_name: str) -> IsNumericChecker:
        ...

    def cat(self, table_name: str, column_name: str) -> IsCategoricalChecker:
        ...

    def id(self, table_name: str, column_name: str) -> IsIdChecker:
        ...

    def date(self, table_name: str, column_name: str) -> IsDateChecker:
        ...

    def char(self, table_name: str, column_name: str) -> IsCharChecker:
        ...

    def run_tests(self) -> list[TestResult]:
        ...

    def __del__(self):
        ...
