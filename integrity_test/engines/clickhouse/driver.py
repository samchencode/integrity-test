from typing import Protocol
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
    ):
        self.client = ClickHouse(
            url=url, port=port, database=database, settings={"use_numpy": True}
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
