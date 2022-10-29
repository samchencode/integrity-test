def make_test_name(table_name: str, column_name: str, test_name) -> str:
    return f"{table_name}.{column_name}::{test_name}"
