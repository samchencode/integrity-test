from unittest.mock import MagicMock
import pytest
from integrity_test.engines.clickhouse.engine import ClickhouseEngine
from integrity_test.engines.clickhouse.driver import StubDriver
from integrity_test.null import Null


def test_instantiation():
    d = StubDriver()
    ClickhouseEngine(d)


@pytest.fixture(scope="function", name="ch_engine")
def fixture_ch_engine(request):
    d = StubDriver()
    d.run_sql = MagicMock(return_value=request.param)
    d.run_sql.reset_mock()
    ch = ClickhouseEngine(d)
    return ch, d.run_sql


@pytest.mark.parametrize(
    "missing_value, sql, ch_engine",
    [
        (
            65535,
            "SELECT count() FROM my_table WHERE my_col != 65535",
            [[0]],
        ),
        (Null, "SELECT count() FROM my_table WHERE my_col IS NOT NULL", [[0]]),
    ],
    indirect=["ch_engine"],
)
def test_num_is_missing(
    missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
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
        (65535, "SELECT count() FROM my_table WHERE my_col = 65535", [[0]]),
        (Null, "SELECT count() FROM my_table WHERE my_col IS NULL", [[0]]),
    ],
    indirect=["ch_engine"],
)
def test_num_not_missing(
    missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.num("my_table", "my_col")
    my_col.n.missing(missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()


@pytest.mark.parametrize(
    "value_range, missing_value, sql, ch_engine",
    [
        (
            (0, 1),
            None,
            "SELECT count() FROM my_table WHERE my_col < 0 OR my_col >= 1",
            [[0]],
        ),
        (
            (-1.0, 1.0),
            Null,
            "SELECT count() FROM my_table WHERE my_col IS NOT NULL AND (my_col < -1.0 OR my_col >= 1.0)",
            [[0]],
        ),
        (
            (-1.0, 1.0),
            999,
            "SELECT count() FROM my_table WHERE my_col != 999 AND (my_col < -1.0 OR my_col >= 1.0)",
            [[0]],
        ),
    ],
    indirect=["ch_engine"],
)
def test_num_in_range(
    value_range, missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.num("my_table", "my_col")
    my_col.in_range(value_range, missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()


@pytest.mark.parametrize(
    "value_range, missing_value, sql, ch_engine",
    [
        (
            (0, 1),
            None,
            "SELECT count() FROM my_table WHERE my_col >= 0 AND my_col < 1",
            [[0]],
        ),
        (
            (-1.0, 1.0),
            Null,
            "SELECT count() FROM my_table WHERE my_col IS NOT NULL AND (my_col >= -1.0 AND my_col < 1.0)",
            [[0]],
        ),
        (
            (-1.0, 1.0),
            999,
            "SELECT count() FROM my_table WHERE my_col != 999 AND (my_col >= -1.0 AND my_col < 1.0)",
            [[0]],
        ),
    ],
    indirect=["ch_engine"],
)
def test_num_not_in_range(
    value_range, missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.num("my_table", "my_col")
    my_col.n.in_range(value_range, missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()


@pytest.mark.parametrize(
    "value_range, missing_value, sql, ch_engine",
    [
        (
            ("1970-01-01", "2149-06-06"),
            None,
            "SELECT count() FROM my_table WHERE my_col < '1970-01-01' OR my_col >= '2149-06-06'",
            [[0]],
        ),
        (
            ("1970-01-01", "2149-06-06"),
            "1925-01-01",
            "SELECT count() FROM my_table WHERE my_col != '1925-01-01' AND (my_col < '1970-01-01' OR my_col >= '2149-06-06')",
            [[0]],
        ),
    ],
    indirect=["ch_engine"],
)
def test_date_in_range(
    value_range, missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.date("my_table", "my_col")
    my_col.in_range(value_range, missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()


@pytest.mark.parametrize(
    "value_range, missing_value, sql, ch_engine",
    [
        (
            ("1970-01-01", "2149-06-06"),
            None,
            "SELECT count() FROM my_table WHERE my_col >= '1970-01-01' AND my_col < '2149-06-06'",
            [[0]],
        ),
        (
            ("1970-01-01", "2149-06-06"),
            "1925-01-01",
            "SELECT count() FROM my_table WHERE my_col != '1925-01-01' AND (my_col >= '1970-01-01' AND my_col < '2149-06-06')",
            [[0]],
        ),
    ],
    indirect=["ch_engine"],
)
def test_date_not_in_range(
    value_range, missing_value, sql, ch_engine: tuple[ClickhouseEngine, MagicMock]
):
    ch, d_run_sql_spy = ch_engine
    my_col = ch.date("my_table", "my_col")
    my_col.n.in_range(value_range, missing_value)
    [res] = ch.run_tests()

    d_run_sql_spy.assert_called_once_with(sql)
    assert res.has_test_passed()
