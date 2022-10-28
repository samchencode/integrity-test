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