from ...protocols import NotCategoricalColumn
from .test_factories import missing, one_of
from ...null import NullType
from .column import ClickHouseColumn


class NotClickHouseCategoricalColumn(ClickHouseColumn):
    def missing(self, missing_value: str):
        factory = missing.NotMissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def one_of(self, values: list[str], missing_value: str | NullType | None = None):
        factory = one_of.NotOneOfCategoricalFactory()
        test = factory.make_test(
            self._table_name, self._column_name, values, missing_value
        )
        self._tests.append(test)


class ClickHouseCategoricalColumn(ClickHouseColumn):
    def __init__(self, table_name: str, column_name: str):
        super().__init__(table_name, column_name)
        self.n: NotCategoricalColumn = NotClickHouseCategoricalColumn(
            table_name, column_name
        )

    def missing(self, missing_value: str):
        factory = missing.MissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def one_of(self, values: list[str], missing_value: str | NullType | None = None):
        factory = one_of.OneOfCategoricalFactory()
        test = factory.make_test(
            self._table_name, self._column_name, values, missing_value
        )
        self._tests.append(test)

    def get_tests(self):
        return self._tests + self.n.get_tests()
