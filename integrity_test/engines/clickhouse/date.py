from ...protocols import NotDateColumn
from .test_factories import missing, in_range
from ...null import NullType
from .column import ClickHouseColumn


class NotClickHouseDateColumn(ClickHouseColumn):
    def missing(self, missing_value: str):
        factory = missing.NotMissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def in_range(
        self,
        value_range: tuple[str, str],
        missing_value: str | NullType | None = None,
    ):
        factory = in_range.NotInRangeDateFactory()
        value_min, value_max = value_range
        test = factory.make_test(
            self._table_name, self._column_name, value_min, value_max, missing_value
        )
        self._tests.append(test)


class ClickHouseDateColumn(ClickHouseColumn):
    def __init__(self, table_name: str, column_name: str):
        super().__init__(table_name, column_name)
        self.n: NotDateColumn = NotClickHouseDateColumn(table_name, column_name)

    def missing(self, missing_value: str):
        factory = missing.MissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def in_range(
        self,
        value_range: tuple[str, str],
        missing_value: str | NullType | None = None,
    ):
        factory = in_range.InRangeDateFactory()
        value_min, value_max = value_range
        test = factory.make_test(
            self._table_name, self._column_name, value_min, value_max, missing_value
        )
        self._tests.append(test)

    def get_tests(self):
        return self._tests + self.n.get_tests()
