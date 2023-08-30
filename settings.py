# Database connection parameters
database_connection = {
    'dbname': 'stockfetcher',
    'user': 'postgres',
    'password': 'pAlcacer9!',
    'host': 'localhost',    # Use the appropriate host if not localhost
    'port': '5432'         # Default PostgreSQL port, change if yours is different
}


# database connection string
DB_CONNECTION_STRING = "dbname=stockfetcher user=postgres password=pAlcacer9! host=localhost port=5432"


# header for authorizing with the SEC
SEC_HEADERS = {
    'User-Agent': 'basti.keil@hotmail.de'
}

