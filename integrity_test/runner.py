from .table import Table
from .interfaces import Engine


class Runner:
    def __init__(self, engine: Engine):
        self._engine = engine
        self._tables: list[Table] = []

    def table(self, table_name: str):
        table = Table(self._engine, table_name)
        self._tables.append(table)
        return table

    def run_tests(self):
        for t in self._tables:
            print("Table Name: " + t.get_name())
            for res in t.run_tests():
                pf = "Pass" if res.has_test_passed() else "Fail"
                print(f"{res.get_name} - {pf} {res.get_message()}")

        del self._engine
