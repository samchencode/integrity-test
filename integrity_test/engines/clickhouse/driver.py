from typing import Any, Protocol
import numpy as np
from clickhouse_driver import Client as ClickHouse


class Driver(Protocol):
    def run_sql(self, sql: str, params: dict = None) -> np.ndarray:
        ...

    def destroy(self):
        ...


class ClickHouseDriver:
    def __init__(
        self,
        database: str,
        url: str = "localhost",
        port: int = 1234,
        settings: dict[str, Any] | None = None,
    ):
        ch_settings = {"use_numpy": True}
        if settings is not None:
            ch_settings = {**ch_settings, **settings}

        self.client = ClickHouse(
            url, port=port, database=database, settings=ch_settings
        )

    def run_sql(self, sql: str, params: dict = None) -> np.ndarray:
        return self.client.execute(sql, params)

    def destroy(self):
        self.client.disconnect()


class StubDriver:
    def run_sql(self, sql: str, params: dict = None) -> np.ndarray:
        pass

    def destroy(self):
        pass
