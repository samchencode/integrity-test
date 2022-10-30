from typing import Callable
from abc import ABC
from ..driver import Driver
from ....test_result import TestResult
from .util import make_test_name


class TestFactory(ABC):
    def _make_test(
        self,
        table_name: str,
        column_name: str,
        test_title: str,
        execute: Callable[[Driver], None],
    ):
        def test(driver: Driver) -> TestResult:
            test_name = make_test_name(table_name, column_name, test_title)
            message = ""
            passing = True
            try:
                execute(driver)
            except Exception as e:
                message = "Error running Test: " + str(e)
                passing = False
            return TestResult(test_name, message, passing)

        return test
