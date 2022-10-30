from .protocols import ClickHouseTest
from ....null import NullType
from ..driver import Driver
from .test_factory import TestFactory


class UniqueFactory(TestFactory):
    def make_test(
        self,
        table_name: str,
        column_name: str,
        missing_value: int | str | NullType | None,
    ) -> ClickHouseTest:
        def execute(driver: Driver):
            result = None
            if missing_value is None:
                result = self._sql_check_unique(driver, table_name, column_name)
            elif isinstance(missing_value, NullType):
                result = self._sql_check_unique_missing_null(
                    driver, table_name, column_name
                )
            else:
                result = self._sql_check_unique_missing_value(
                    driver, table_name, column_name, missing_value
                )
            if len(result) > 0:
                raise Exception("Some values are not unique!")

        return self._make_test(table_name, column_name, "is_unique", execute)

    def _sql_check_unique(self, driver: Driver, table_name: str, column_name: str):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"GROUP BY {column_name} "
            f"HAVING count() > 1 LIMIT 1"
        )

    def _sql_check_unique_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        missing_value: int | str,
    ):
        sql_missing_value_str = (
            str(missing_value)
            if not isinstance(missing_value, str)
            else f"'{missing_value}'"
        )
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != {sql_missing_value_str} "
            f"GROUP BY {column_name} "
            f"HAVING count() > 1 LIMIT 1"
        )

    def _sql_check_unique_missing_null(
        self, driver: Driver, table_name: str, column_name: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"GROUP BY {column_name} "
            f"HAVING count() > 1 LIMIT 1"
        )


class NotUniqueFactory(UniqueFactory):
    def make_test(
        self,
        table_name: str,
        column_name: str,
        missing_value: int | str | NullType | None,
    ) -> ClickHouseTest:
        def execute(driver: Driver):
            result = None
            if missing_value is None:
                result = self._sql_check_unique(driver, table_name, column_name)
            elif isinstance(missing_value, NullType):
                result = self._sql_check_unique_missing_null(
                    driver, table_name, column_name
                )
            else:
                result = self._sql_check_unique_missing_value(
                    driver, table_name, column_name, missing_value
                )

            if len(result) < 1:
                raise Exception("All values are unique!")

        return self._make_test(table_name, column_name, "not.is_unique", execute)
