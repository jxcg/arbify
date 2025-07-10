from data.pg_connector import PostgresDB


def get_db():
    return PostgresDB(
        dbname='arbifydb',
        user='arbuser',
        password='temp_secure_44',
        host='143.47.226.107',
        port=5432
    )
