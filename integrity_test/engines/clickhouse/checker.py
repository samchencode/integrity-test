from typing import Callable
from .driver import Driver
from ...test_result import TestResult

ClickhouseTest = Callable[[Driver], TestResult]


class NotClickHouseNumericChecker:
    def __init__(self, table_name: str, column_name: str):
        self._table_name = table_name
        self._column_name = column_name
        self._tests: list[ClickhouseTest] = []

    def missing(self, missing_value: int | str | None):
        def test(driver: Driver) -> TestResult:
            test_name = self.__class__.__name__ + ".missing"
            message = ""
            has_passed = True
            result = None
            try:
                [[result]] = (
                    self._sql_check_missing_value(driver, missing_value)
                    if missing_value is not None
                    else self._sql_check_missing_null(driver)
                )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                has_passed = False
            if result != 0:
                message = f"Some rows are missing! {result} rows equal {missing_value}"
                has_passed = False

            return TestResult(test_name, message, has_passed)

        self._tests.append(test)

    def _sql_check_missing_value(self, driver: Driver, missing_value: int | str):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        res = driver.run_sql(
            f"SELECT count() FROM {self._table_name} "
            f"WHERE {self._column_name} = {sql_esc_missing_val} "
        )
        print(res)
        return res

    def _sql_check_missing_null(self, driver: Driver):
        return driver.run_sql(
            f"SELECT count() FROM {self._table_name} "
            f"WHERE {self._column_name} IS NULL "
        )

    def get_tests(self):
        return self._tests


class ClickHouseNumericChecker:
    def __init__(self, table_name: str, column_name: str):
        self._table_name = table_name
        self._column_name = column_name
        self._tests: list[ClickhouseTest] = []
        self.n = NotClickHouseNumericChecker(table_name, column_name)

    def missing(self, missing_value: int | str | None):
        def test(driver: Driver) -> TestResult:
            test_name = self.__class__.__name__ + ".missing"
            message = ""
            has_passed = True
            result = None
            try:
                [[result]] = (
                    self._sql_check_missing_value(driver, missing_value)
                    if missing_value is not None
                    else self._sql_check_missing_null(driver)
                )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                has_passed = False

            if result != 0:
                message = (
                    f"Not all rows are missing! {result} rows equal {missing_value}"
                )
                has_passed = False

            return TestResult(
                test_name=test_name, message=message, has_passed=has_passed
            )

        self._tests.append(test)

    def _sql_check_missing_value(self, driver: Driver, missing_value: int | str):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        return driver.run_sql(
            f"SELECT count() FROM {self._table_name} "
            f"WHERE {self._column_name} != {sql_esc_missing_val} "
        )

    def _sql_check_missing_null(self, driver: Driver):
        return driver.run_sql(
            f"SELECT count() FROM {self._table_name} "
            f"WHERE {self._column_name} IS NOT NULL "
        )

    def get_tests(self):
        return self._tests + self.n.get_tests()
