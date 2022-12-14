# Integrity Test

Automated integrity testing of data with python.

# Up and Running

1. `pipenv install`
2. To activate this project's virtualenv, run `pipenv shell`.
    Alternatively, run a command inside the virtualenv with `pipenv run`.

# Types of Integrity

1. Entity Integrity
  - Non-Null ?Unique Primary Key
  - Correct dtype
  - Values formatted correctly

2. Domain Integrity
  - Column that should have unique values do have unique values
  - Non-Null columns don't have nulls or missing values
  - Ranges of values are as expected. (ie no 200 year olds)

3. Referential Integrity
  - Foreign Key 

# Usage (hopefully)

```python
from integrity_test.runner import Runner
from integrity_test.engines.clickhouse import driver, engine

d = driver.ClickHouseDriver(database="old")
e = engine.ClickHouseEngine(d)
runner = Runner(e)

patients = runner.table("patients")

patient_id = patients.id("patient_id")
patient_id.unique()
patient_id.n.missing("")
```

# Ideas to add

1. Check categorical columns have at least one of each possible value...