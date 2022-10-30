from ..driver import Driver
from .test_factory import TestFactory


class InReferenceToFactory(TestFactory):
    def make_test(
        self,
        table_name: str,
        column_name: str,
        other_table_name: str,
        other_column_name: str,
    ):
        def execute(driver: Driver):
            [[result]] = self._sql_check_in_reference_to(
                driver, table_name, column_name, other_table_name, other_column_name
            )
            if result > 0:
                raise Exception(
                    f"Referential integrity violation! {result} unique ids in {column_name} not found in {other_column_name}"
                )

        return self._make_test(table_name, column_name, "is_in_reference_to", execute)

    def _sql_check_in_reference_to(
        self,
        driver: Driver,
        table_name: str,
        column_name: str,
        other_table_name: str,
        other_column_name: str,
    ):
        return driver.run_sql(
            f"SELECT count() FROM {table_name} AS a "
            f"LEFT ANY JOIN {other_table_name} AS b "
            f"ON a.{column_name} = b.{other_column_name} "
            f"WHERE a.{column_name} = ''"
        )
