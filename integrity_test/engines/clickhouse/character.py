from ...protocols import NotCharColumn
from .test_factories import missing, match
from ...null import NullType
from .column import ClickHouseColumn


class NotClickhouseCharColumn(ClickHouseColumn):
    def missing(self, missing_value: str | NullType):
        factory = missing.NotMissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def match(self, pattern: str, missing_value: str | NullType | None = None):
        factory = match.NotMatchCharFactory()
        test = factory.make_test(
            self._table_name, self._column_name, pattern, missing_value
        )
        self._tests.append(test)


class ClickhouseCharColumn(ClickHouseColumn):
    def __init__(self, table_name: str, column_name: str):
        super().__init__(table_name, column_name)
        self.n: NotCharColumn = NotClickhouseCharColumn(table_name, column_name)

    def missing(self, missing_value: str | NullType):
        factory = missing.MissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def match(self, pattern: str, missing_value: str | NullType | None = None):
        factory = match.MatchCharFactory()
        test = factory.make_test(
            self._table_name, self._column_name, pattern, missing_value
        )
        self._tests.append(test)

    def get_tests(self):
        return super().get_tests() + self.n.get_tests()
