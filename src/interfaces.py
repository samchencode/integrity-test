from typing import Protocol, Callable
from .test_result import TestResult

Test = Callable[[], TestResult]


class Checker(Protocol):
    def _get_tests(self) -> list[Test]:
        ...


class NumericChecker(Checker, Protocol):
    def missing(self, missing_value: int):
        ...

    def in_range(self, value_range: tuple[int | float, int | float], na_value: str):
        ...


class IsntNumericChecker(NumericChecker, Protocol):
    ...


class IsNumericChecker(NumericChecker, Protocol):
    isnt: IsntNumericChecker


class DateChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def in_range(self, value_range: tuple[str, str], na_value: str):
        ...


class IsntDateChecker(DateChecker, Protocol):
    ...


class IsDateChecker(DateChecker, Protocol):
    isnt: IsntDateChecker


class CategoricalChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def one_of(self, values: list[str]):
        ...


class IsntCategoricalChecker(CategoricalChecker, Protocol):
    ...


class IsCategoricalChecker(CategoricalChecker, Protocol):
    isnt: IsntCategoricalChecker


class IdChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def unique(self):
        ...

    def in_reference_to(self, table_name: str, column_name: str):
        ...


class IsntIdChecker(IdChecker, Protocol):
    ...


class IsIdChecker(IdChecker, Protocol):
    isnt: IsntIdChecker


class CharChecker(Checker, Protocol):
    def missing(self, missing_value: str):
        ...

    def match(self, pattern=str):
        ...


class IsntCharChecker(CharChecker, Protocol):
    ...


class IsCharChecker(CharChecker, Protocol):
    isnt: IsntCharChecker


class Engine(Protocol):
    def num(self, column_name: str) -> IsNumericChecker:
        ...

    def cat(self, column_name: str) -> IsCategoricalChecker:
        ...

    def id(self, column_name: str) -> IsIdChecker:
        ...

    def date(self, column_name: str) -> IsDateChecker:
        ...

    def char(self, column_name: str) -> IsCharChecker:
        ...

    def get_tests(self) -> list[Test]:
        ...

    def destroy(self):
        ...
