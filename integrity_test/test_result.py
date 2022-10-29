class TestResult:
    def __init__(self, test_name: str, message: str, has_passed: bool):
        self._test_name: str = test_name
        self._message: str = message
        self._has_passed: bool = has_passed

    def get_name(self) -> str:
        return self._test_name

    def get_message(self) -> str:
        return self._message

    def has_test_passed(self) -> bool:
        return self._has_passed
