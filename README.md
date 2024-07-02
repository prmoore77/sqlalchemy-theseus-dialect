# SQLAlchemy [Theseus]((https://voltrondata.com/theseus.html)) Dialect - powered by Arrow Flight SQL ADBC 

[<img src="https://img.shields.io/badge/GitHub-prmoore77%2Fsqlalchemy--theseus--dialect-blue.svg?logo=Github">](https://github.com/prmoore77/sqlalchemy-theseus-dialect)
[![sqlalchemy-theseus-dialect-ci](https://github.com/prmoore77/sqlalchemy-theseus-dialect/actions/workflows/ci.yml/badge.svg)](https://github.com/prmoore77/sqlalchemy-theseus-dialect/actions/workflows/ci.yml)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/sqlalchemy--theseus--dialect)](https://pypi.org/project/sqlalchemy-theseus-dialect/)
[![PyPI version](https://badge.fury.io/py/sqlalchemy-theseus-dialect.svg)](https://badge.fury.io/py/sqlalchemy-theseus-dialect)
[![PyPI Downloads](https://img.shields.io/pypi/dm/sqlalchemy--flight--sql--adbc--dialect.svg)](https://pypi.org/project/sqlalchemy-theseus-dialect/)

Basic SQLAlchemy dialect for [the Theseus Data Processing Engine](https://voltrondata.com/theseus.html)

## Installation

### Option 1 - from PyPi
```sh
$ pip install sqlalchemy-theseus-dialect
```

### Option 2 - from source - for development
```shell
git clone https://github.com/prmoore77/sqlalchemy-theseus-dialect

cd sqlalchemy-theseus-dialect

# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
. .venv/bin/activate

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install SQLAlchemy Theseus Dialect - in editable mode with dev dependencies
pip install --editable .[dev]
```

### Note
For the following commands - if you running from source and using `--editable` mode (for development purposes) - you will need to set the PYTHONPATH environment variable as follows:
```shell
export PYTHONPATH=$(pwd)/src
```

## Usage

Once you've installed this package, you should be able to just use it, as SQLAlchemy does a python path search

### Ensure you have access to a Theseus engine

### Connect with the SQLAlchemy Theseus Dialect
```python
import logging

from sqlalchemy import create_engine, MetaData, Table, select, Column, text, Integer, String, Sequence
from sqlalchemy.orm import Session
from sqlalchemy.engine.url import URL

# Setup logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def main():
    # Build the URL
    url = URL.create(drivername="theseus",
                     host="theseus-gateway.vice.svc.cluster.local",
                     port=11234,
                     query={"disableCertificateVerification": "True",
                            "useEncryption": "False"
                            }
                     )

    print(f"Database URL: {url}")

    engine = create_engine(url=url)

    metadata = MetaData()
    metadata.reflect(bind=engine)

    for table_name in metadata.tables:
        print(f"Table name: {table_name}")

    with Session(bind=engine) as session:

        # Execute some raw SQL (this assumes you have a registered table called: "fake")
        results = session.execute(statement=text("SELECT * FROM fake")).fetchall()
        print(results)

        # Try a SQLAlchemy table select
        fake: Table = metadata.tables["fake"]
        stmt = select(fake.c.name)

        results = session.execute(statement=stmt).fetchall()
        print(results)


if __name__ == "__main__":
    main()
```

### Credits
Much code and inspiration was taken from repo: https://github.com/Mause/duckdb_engine
