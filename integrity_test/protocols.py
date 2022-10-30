from typing import Protocol, Callable, Generic, TypeVar
from .test_result import TestResult
from .null import Null, NullType

T = TypeVar("T")

Test = Callable[[T], TestResult]


class Column(Protocol, Generic[T]):
    def get_tests(self) -> list[Test[T]]:
        ...


class NumericColumn(Column, Protocol):
    def missing(self, missing_value: int | str | NullType):
        ...

    def in_range(
        self,
        value_range: tuple[int | float, int | float],
        missing_value: int | str | NullType | None,
    ):
        ...


class NotNumericColumn(NumericColumn, Protocol):
    ...


class IsNumericColumn(NumericColumn, Protocol):
    n: NotNumericColumn


class DateColumn(Column, Protocol):
    def missing(self, missing_value: str):
        ...

    def in_range(
        self, value_range: tuple[str, str], missing_value: str | NullType | None = None
    ):
        ...


class NotDateColumn(DateColumn, Protocol):
    ...


class IsDateColumn(DateColumn, Protocol):
    n: NotDateColumn


class CategoricalColumn(Column, Protocol):
    def missing(self, missing_value: str):
        ...

    def one_of(self, values: list[str], missing_value: str | NullType | None = None):
        ...


class NotCategoricalColumn(CategoricalColumn, Protocol):
    ...


class IsCategoricalColumn(CategoricalColumn, Protocol):
    n: NotCategoricalColumn


class IdColumn(Column, Protocol):
    def missing(self, missing_value: str):
        ...

    def unique(self):
        ...


class NotIdColumn(IdColumn, Protocol):
    ...


class IsIdColumn(IdColumn, Protocol):
    n: NotIdColumn

    def in_reference_to(self, table_name: str, column_name: str):
        ...


class CharColumn(Column, Protocol):
    def missing(self, missing_value: str | NullType):
        ...

    def match(self, pattern: str, missing_value: str | NullType | None = None):
        ...


class NotCharColumn(CharColumn, Protocol):
    ...


class IsCharColumn(CharColumn, Protocol):
    n: NotCharColumn


class Engine(Protocol):
    def num(self, table_name: str, column_name: str) -> IsNumericColumn:
        ...

    def cat(self, table_name: str, column_name: str) -> IsCategoricalColumn:
        ...

    def id(self, table_name: str, column_name: str) -> IsIdColumn:
        ...

    def date(self, table_name: str, column_name: str) -> IsDateColumn:
        ...

    def char(self, table_name: str, column_name: str) -> IsCharColumn:
        ...

    def run_tests(self) -> list[TestResult]:
        ...

    def __del__(self):
        ...
