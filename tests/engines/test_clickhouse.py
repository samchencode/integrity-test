from unittest.mock import MagicMock
import pytest
from integrity_test.engines.clickhouse import engine, driver
from integrity_test.null import Null


def test_instantiation():
    d = driver.StubDriver()
    engine.ClickhouseEngine(d)


@pytest.fixture(scope="function", name="ch_engine")
def fixture_ch_engine(request):
    d = driver.StubDriver()
    d.run_sql = MagicMock(return_value=request.param)
    d.run_sql.reset_mock()
    ch = engine.ClickhouseEngine(d)
    return ch, d.run_sql


@pytest.mark.parametrize(
    "missing_value, sql, ch_engine",
    [
        (
            65535,
            "SELECT count() FROM my_table WHERE my_col != 65535 ",
            [[0]],
        ),
        (Null, "SELECT count() FROM my_table WHERE my_col IS NOT NULL ", [[0]]),
    ],
    indirect=["ch_engine"],
)
def test_num_is_missing(
    missing_value, sql, ch_engine: tuple[engine.ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.num("my_table", "my_col")
    my_col.missing(missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()


@pytest.mark.parametrize(
    "missing_value, sql, ch_engine",
    [
        (65535, "SELECT count() FROM my_table WHERE my_col = 65535 ", [[0]]),
        (Null, "SELECT count() FROM my_table WHERE my_col IS NULL ", [[0]]),
    ],
    indirect=["ch_engine"],
)
def test_num_not_missing(
    missing_value, sql, ch_engine: tuple[engine.ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.num("my_table", "my_col")
    my_col.n.missing(missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()
