import pandas as pd
import psycopg2
from psycopg2.extras import execute_values


def bulk_insert_on_duplicate_update(dataframe, table_name, unique_keys, conn_str):
    """
    Performs a bulk insert with "on duplicate key update" operation on a PostgreSQL database using a temp table.

    Parameters:
    - dataframe: The pandas DataFrame to be inserted
    - table_name: Name of the table in the database
    - unique_keys: A list of columns that constitute the unique key for conflict resolution
    - conn_str: Connection string for the database

    Returns:
    - None
    """

    # Convert dataframe to list of dictionaries
    records = dataframe.to_dict(orient='records')

    # Create INSERT query for temp table
    columns = dataframe.columns
    temp_table_name = table_name + "_temp"
    create_temp_table_query = f"CREATE TEMP TABLE {temp_table_name} AS SELECT * FROM {table_name} WITH NO DATA;"
    insert_temp_table_query = f"INSERT INTO {temp_table_name} ({','.join(columns)}) VALUES %s"

    # Create ON DUPLICATE KEY UPDATE query
    update_query = f"""
    INSERT INTO {table_name} ({','.join(columns)})
    SELECT {','.join(columns)} FROM {temp_table_name}
    ON CONFLICT ({', '.join(unique_keys)}) DO UPDATE SET 
    """
    update_query += ", ".join([f"{col}=EXCLUDED.{col}" for col in columns if col not in unique_keys])

    # Convert the list of dictionaries to a list of tuples for the INSERT operation
    values = [tuple(record.values()) for record in records]

    # Connect to the database
    with psycopg2.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_temp_table_query)
            execute_values(cursor, insert_temp_table_query, values)
            cursor.execute(update_query)
            cursor.execute(f"DROP TABLE {temp_table_name};")  # Clean up the temp table

    return None
