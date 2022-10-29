from typing import Callable
from ....test_result import TestResult
from ..driver import Driver

ClickHouseTest = Callable[[Driver], TestResult]
