from integrity_test.engines.clickhouse.test_factories import missing
from ....null import NullType
from .util import make_test_name
from .protocols import ClickHouseTest
from ....test_result import TestResult
from ..driver import Driver


class InRangeNumericFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
        missing_value: int | str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver):
            test_name = make_test_name(table_name, column_name, "is_in_range")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_in_range(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_in_range_missing_null(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                else:
                    [[result]] = self._sql_check_in_range_missing_value(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                        missing_value,
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"{result} rows are not in range [{value_min}, {value_max})"
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_in_range(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} < {value_min} OR {column_name} >= {value_max}"
        )

    def _sql_check_in_range_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND ({column_name} < {value_min} OR {column_name} >= {value_max})"
        )

    def _sql_check_in_range_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
        missing_value: int | str,
    ):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != {sql_esc_missing_val} "
            f"AND ({column_name} < {value_min} OR {column_name} >= {value_max})"
        )


class NotInRangeNumericFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
        missing_value: int | str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver):
            test_name = make_test_name(table_name, column_name, "not.is_in_range")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_in_range(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_in_range_missing_null(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                else:
                    [[result]] = self._sql_check_in_range_missing_value(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                        missing_value,
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"{result} rows are not in range [{value_min}, {value_max})"
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_in_range(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} >= {value_min} AND {column_name} < {value_max}"
        )

    def _sql_check_in_range_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND ({column_name} >= {value_min} AND {column_name} < {value_max})"
        )

    def _sql_check_in_range_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: int | float,
        value_max: int | float,
        missing_value: int | str,
    ):
        sql_esc_missing_val = str(missing_value)
        if isinstance(missing_value, str):
            sql_esc_missing_val = "'" + missing_value + "'"
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != {sql_esc_missing_val} "
            f"AND ({column_name} >= {value_min} AND {column_name} < {value_max})"
        )


class InRangeDateFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
        missing_value: str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver):
            test_name = make_test_name(table_name, column_name, "is_in_range")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_in_range(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_in_range_missing_null(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                else:
                    [[result]] = self._sql_check_in_range_missing_value(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                        missing_value,
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"{result} rows are not in range [{value_min}, {value_max})"
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_in_range(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} < '{value_min}' OR {column_name} >= '{value_max}'"
        )

    def _sql_check_in_range_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND ({column_name} < '{value_min}' OR {column_name} >= '{value_max}')"
        )

    def _sql_check_in_range_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
        missing_value: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != '{missing_value}' "
            f"AND ({column_name} < '{value_min}' OR {column_name} >= '{value_max}')"
        )


class NotInRangeDateFactory:
    def make_test(
        self,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
        missing_value: str | NullType | None,
    ) -> ClickHouseTest:
        def test(driver: Driver):
            test_name = make_test_name(table_name, column_name, "not.is_in_range")
            message = ""
            passing = True
            result = None
            try:
                if missing_value is None:
                    [[result]] = self._sql_check_in_range(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                elif isinstance(missing_value, NullType):
                    [[result]] = self._sql_check_in_range_missing_null(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                    )
                else:
                    [[result]] = self._sql_check_in_range_missing_value(
                        driver,
                        table_name,
                        column_name,
                        value_min,
                        value_max,
                        missing_value,
                    )
            except Exception as e:
                message = "Error running SQL: " + str(e)
                passing = False
            if result != 0:
                message = f"{result} rows are not in range [{value_min}, {value_max})"
                passing = False

            return TestResult(test_name, message, passing)

        return test

    def _sql_check_in_range(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} >= '{value_min}' AND {column_name} < '{value_max}'"
        )

    def _sql_check_in_range_missing_null(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} IS NOT NULL "
            f"AND ({column_name} >= '{value_min}' AND {column_name} < '{value_max}')"
        )

    def _sql_check_in_range_missing_value(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        value_min: str,
        value_max: str,
        missing_value: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} "
            f"WHERE {column_name} != '{missing_value}' "
            f"AND ({column_name} >= '{value_min}' AND {column_name} < '{value_max}')"
        )
