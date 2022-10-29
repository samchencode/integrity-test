from typing import Protocol
import numpy as np
from clickhouse_driver import Client as ClickHouse


class Driver(Protocol):
    def executeSql(self, sql: str, params: dict) -> np.ndarray:
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

    def executeSql(self, sql: str, params: dict) -> np.ndarray:
        return self.client.execute(sql, params)

    def destroy(self):
        self.client.disconnect()
