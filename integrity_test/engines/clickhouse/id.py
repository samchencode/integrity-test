from integrity_test.protocols import NotIdColumn
from .test_factories import missing, unique, in_reference_to
from .column import ClickHouseColumn


class NotClickHouseIdColumn(ClickHouseColumn):
    def missing(self, missing_value: str):
        factory = missing.NotMissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def unique(self):
        factory = unique.NotUniqueFactory()
        test = factory.make_test(self._table_name, self._column_name, None)
        self._tests.append(test)


class ClickHouseIdColumn(ClickHouseColumn):
    def __init__(self, table_name: str, column_name: str):
        super().__init__(table_name, column_name)
        self.n: NotIdColumn = NotClickHouseIdColumn(table_name, column_name)

    def missing(self, missing_value: str):
        factory = missing.MissingFactory()
        test = factory.make_test(self._table_name, self._column_name, missing_value)
        self._tests.append(test)

    def unique(self):
        factory = unique.UniqueFactory()
        test = factory.make_test(self._table_name, self._column_name, None)
        self._tests.append(test)

    def in_reference_to(self, table_name: str, column_name: str):
        factory = in_reference_to.InReferenceToFactory()
        test = factory.make_test(
            self._table_name, self._column_name, table_name, column_name
        )
        self._tests.append(test)

    def get_tests(self):
        return super().get_tests() + self.n.get_tests()
