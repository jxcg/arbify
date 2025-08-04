import toml
from data.pg_connector import PostgresDB


def get_db():
    secrets = toml.load(".streamlit/secrets.toml")
    db_details = secrets.get('database')
    return PostgresDB(
        dbname=db_details.get('dbname'),
        user=db_details.get('user'),
        password=db_details.get('password'),
        host=db_details.get('host'),
        port=db_details.get('port')
    )

