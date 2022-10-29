from .protocols import ClickHouseTest
from ....test_result import TestResult
from ..driver import Driver
from .util import make_test_name


class MissingFactory:
    def make_test(
        self, table_name: str, column_name: str, missing_value: int | str | None
    ) -> ClickHouseTest:
        def test(driver: Driver) -> TestResult:
            test_name = make_test_name(table_name, column_name, "is_missing")
            message = ""
            passing = True
            result = None
            try:
                [[result]] = (
                    self._sql_check_missing_value(
                        driver, table_name, column_name, missing_value
                    )
                    if missing_value is not None
                    else self._sql_check_missing_null(driver, table_name, column_name)
                )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = (
                    f"Not all rows are missing! {result} rows equal {missing_value}"
                )
                passing = False

            return TestResult(test_name=test_name, message=message, has_passed=passing)

        return test

    def _sql_check_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        missing_value: int | str,
    ):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != {sql_esc_missing_val} "
        )

    def _sql_check_missing_null(
        self, driver: Driver, table_name: str, column_name: str
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} " f"WHERE {column_name} IS NOT NULL "
        )


class NotMissingFactory:
    def make_test(
        self, table_name: str, column_name: str, missing_value: int | str | None
    ) -> ClickHouseTest:
        def test(driver: Driver) -> TestResult:
            test_name = make_test_name(table_name, column_name, "not.is_missing")
            message = ""
            passing = True
            result = None
            try:
                [[result]] = (
                    self._sql_check_missing_value(
                        driver, table_name, column_name, missing_value
                    )
                    if missing_value is not None
                    else self._sql_check_missing_null(driver, table_name, column_name)
                )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"Some rows are missing! {result} rows equal {missing_value}"
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        missing_value: int | str,
    ):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        res = driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} = {sql_esc_missing_val} "
        )
        print(res)
        return res

    def _sql_check_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} " f"WHERE {column_name} IS NULL "
        )
