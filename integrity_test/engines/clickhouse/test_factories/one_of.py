from .protocols import ClickHouseTest
from ....null import NullType
from ....test_result import TestResult
from ..driver import Driver
from .util import make_test_name


class OneOfCategoricalFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        values: list[str],
        missing_value: str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver) -> TestResult:
            test_name = make_test_name(table_name, column_name, "is_one_of")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_one_of(
                        driver, table_name, column_name, values
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_one_of_missing_null(
                        driver, table_name, column_name, values
                    )
                else:
                    [[result]] = self._sql_check_one_of_missing_value(
                        driver, table_name, column_name, values, missing_value
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"Not all values are one of {str(values)}! {result} have other values."
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_one_of(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} NOT IN ({sql_values_str})"
        )

    def _sql_check_one_of_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
        missing_value: str,
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != '{missing_value}' "
            f"AND {column_name} NOT IN ({sql_values_str})"
        )

    def _sql_check_one_of_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND {column_name} NOT IN ({sql_values_str})"
        )


class NotOneOfCategoricalFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        values: list[str],
        missing_value: str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver) -> TestResult:
            test_name = make_test_name(table_name, column_name, "not.is_one_of")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_one_of(
                        driver, table_name, column_name, values
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_one_of_missing_null(
                        driver, table_name, column_name, values
                    )
                else:
                    [[result]] = self._sql_check_one_of_missing_value(
                        driver, table_name, column_name, values, missing_value
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"Some values are one of {str(values)}! {result} have one of those values."
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_one_of(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IN ({sql_values_str})"
        )

    def _sql_check_one_of_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
        missing_value: str,
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != {missing_value} "
            f"AND {column_name} IN ({sql_values_str})"
        )

    def _sql_check_one_of_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        values: list[str],
    ):
        sql_values_str = ", ".join([f"'{v}'" for v in values])
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND {column_name} IN ({sql_values_str})"
        )
