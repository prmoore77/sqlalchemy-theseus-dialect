import os
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
