import psycopg2

class PostgresDB:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Connected to the database.")
            self.cursor.execute("SET search_path TO bethistory;")
        except psycopg2.Error as e:
            print(f"Connection error: {e}")
            raise
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")



    def execute(self, query, params=None):
        """
        Executes a SQL query. Returns result if query includes RETURNING or is a SELECT.
        """
        try:
            self.cursor.execute(query, params)

            lowered = query.strip().lower()
            if lowered.startswith("select") or "returning" in lowered:
                return self.cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Query error: {e}")
            return None



