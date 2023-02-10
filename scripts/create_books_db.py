import logging
import os
import sys

from dotenv import load_dotenv
from postgres_database_utils import create_connection, PostgresCredentials

# constants
DROP_TABLE = True
TABLE_NAME = "books"

logger = logging.getLogger(f"{TABLE_NAME}_db")
logger.setLevel(logging.INFO)
# logger.addHandler(logging.FileHandler(f"{TABLE_NAME}_db.log"))
logger.addHandler(logging.StreamHandler(sys.stdout))

load_dotenv()


def main() -> None:
    logger.info("Loading environment variables...")

    credentials = PostgresCredentials(
        host=os.environ.get("DATABASE_HOST"),
        database=os.environ.get("DATABASE_NAME"),
        user=os.environ.get("DATABASE_USER"),
        password=os.environ.get("DATABASE_PASSWORD"),
    )

    connection = create_connection(credentials)
    cursor = connection.cursor()

    drop_table = f"""DROP TABLE IF EXISTS {TABLE_NAME};"""

    create_table = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            {TABLE_NAME}_id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL,
            created TIMESTAMPTZ DEFAULT timezone('utc', NOW()) NOT NULL,
            value FLOAT NOT NULL,
            metadata JSONB NOT NULL
        );
    """

    indexes = [
        f"CREATE INDEX {TABLE_NAME}_created_idx ON {TABLE_NAME} (created);",
        f"CREATE INDEX {TABLE_NAME}_title_idx ON {TABLE_NAME} (title);",
    ]

    try:
        if DROP_TABLE:
            cursor.execute(drop_table)
            logger.info(f"Dropped table {TABLE_NAME}")
        cursor.execute(create_table)
        for index in indexes:
            cursor.execute(index)
        connection.commit()
        print(f"{TABLE_NAME} table created successfully.")
    except Exception as error:
        if connection:
            connection.rollback()
        print("Error while connecting to PostgreSQL", error)
        print("Table creation failed.")
    finally:
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
