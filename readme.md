[![Maintainability](https://api.codeclimate.com/v1/badges/25cf8913fbec3dfd4d1e/maintainability)](https://codeclimate.com/github/ZelieM/MT-planting_planner/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/25cf8913fbec3dfd4d1e/test_coverage)](https://codeclimate.com/github/ZelieM/MT-planting_planner/test_coverage)
[![Build Status](https://travis-ci.org/ZelieM/MT-planting_planner.svg?branch=master)](https://travis-ci.org/ZelieM/MT-planting_planner)

# Description

Todo small description of the project and the architecture

# Installation

### Requirements
- Install [python3](https://www.python.org/)
- Install [PostgreSQL](https://www.postgresql.org)
- (pip should be installed along with python3 but if is not the case, install it as well)
- Install required dependencies with `pip install -r requirements.txt`
- Create  Postgre database named `planting_planner_db`
- Create a Postgre database named `vegetable_library_db`
- Create a Postgre user named `postgres` with password `azerty` and grant him full access to both databases

### Migrations
Execute the migrations on the databases with the following commands:
- `python manage.py migrate`
- `python manage.py migrate --database=db_vegetables_library`

# Development

To develop this project locally, install the requirements (see above).

Then start the project locally with

```
python manage.py runserver
```

# Tests
To run the unit tests with code coverage, execute

```
coverage run --source='.' manage.py test planner
```
