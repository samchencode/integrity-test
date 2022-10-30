from .test_factory import TestFactory
from ....null import NullType
from ..driver import Driver


class MatchCharFactory(TestFactory):
    def make_test(
        self,
        table_name: str,
        column_name: str,
        pattern: str,
        missing_value: str | NullType | None,
    ):
        def execute(driver: Driver):
            result = None
            if missing_value is None:
                [[result]] = self._sql_check_match(
                    driver, table_name, column_name, pattern
                )
            elif isinstance(missing_value, NullType):
                [[result]] = self._sql_check_match_missing_null(
                    driver, table_name, column_name, pattern
                )
            else:
                [[result]] = self._sql_check_match_missing_value(
                    driver, table_name, column_name, pattern, missing_value
                )

            if result > 0:
                raise Exception("{result} rows do not match!")

        return self._make_test(table_name, column_name, "is_match", execute)

    def _sql_check_match(
        self, driver: Driver, table_name: str, column_name: str, pattern: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} NOT LIKE '{pattern}'"
        )

    def _sql_check_match_missing_null(
        self, driver: Driver, table_name: str, column_name: str, pattern: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} NOT LIKE '{pattern}' "
            f"AND {column_name} IS NOT NULL"
        )

    def _sql_check_match_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        pattern: str,
        missing_value: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} NOT LIKE '{pattern}' "
            f"AND {column_name} != '{missing_value}'"
        )


class NotMatchCharFactory(TestFactory):
    def make_test(
        self,
        table_name: str,
        column_name: str,
        pattern: str,
        missing_value: str | NullType | None,
    ):
        def execute(driver: Driver):
            result = None
            if missing_value is None:
                [[result]] = self._sql_check_match(
                    driver, table_name, column_name, pattern
                )
            elif isinstance(missing_value, NullType):
                [[result]] = self._sql_check_match_missing_null(
                    driver, table_name, column_name, pattern
                )
            else:
                [[result]] = self._sql_check_match_missing_value(
                    driver, table_name, column_name, pattern, missing_value
                )

            if result > 0:
                raise Exception("Some rows match. {result} rows do match!")

        return self._make_test(table_name, column_name, "not.is_match", execute)

    def _sql_check_match(
        self, driver: Driver, table_name: str, column_name: str, pattern: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} " f"WHERE {column_name} LIKE '{pattern}'"
        )

    def _sql_check_match_missing_null(
        self, driver: Driver, table_name: str, column_name: str, pattern: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} LIKE '{pattern}' "
            f"AND {column_name} IS NOT NULL"
        )

    def _sql_check_match_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        pattern: str,
        missing_value: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} LIKE '{pattern}' "
            f"AND {column_name} != '{missing_value}'"
        )
