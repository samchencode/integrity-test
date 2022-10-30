from unittest.mock import MagicMock
from integrity_test.engines.clickhouse.engine import ClickHouseEngine
from integrity_test.engines.clickhouse.driver import StubDriver
from integrity_test.runner import Runner


def test_instantiation():
    d = StubDriver()
    e = ClickHouseEngine(d)
    Runner(e)


def test_num_is_missing():
    d = StubDriver()
    d.run_sql = MagicMock(return_value=[[0]])
    d.run_sql.reset_mock()
    ch = ClickHouseEngine(d)
    runner = Runner(ch)

    my_table = runner.table("my_table")
    my_col = my_table.num("my_col")
    my_col.in_range([0, 1])

    [res] = my_table.run_tests()

    d.run_sql.assert_called_once_with(
        "SELECT count() FROM my_table WHERE my_col < 0 OR my_col >= 1"
    )
    assert res.has_test_passed()
