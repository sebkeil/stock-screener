'''
We need to create a mapping from Fundamental Accounting Concepts to GAAP tags

Links:
    - http://accounting.auditchain.finance/reporting-scheme/us-gaap/fac/Rules_Mapping/ConceptMap_General-mapping.html

toDO: how can we keep this updated with recent GAAP taxonomies?

'''

import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
from logger import logger


if __name__ == '__main__':
    response = requests.get('http://accounting.auditchain.finance/reporting-scheme/us-gaap/fac/Rules_Mapping/ConceptMap_General-mapping.html')
    soup = BeautifulSoup(response.content, 'html.parser')

    # Locate the table
    table = soup.find('table')

    # Get table headers
    headers = [th.text for th in table.find('tr').find_all('th')]

    # Extract rows from the table
    rows = table.find_all('tr')[1:]  # the first row is usually the header, so skip it
    table_data = []

    for row in rows:
        current_row = [td.text for td in row.find_all('td')]
        if len(current_row) != 5:
            print('NEIN!!')

        print(len(current_row))
        table_data.append(current_row)

    # convert to dataframe
    df = pd.DataFrame(table_data, columns=headers)

    # Create a connection to the PostgreSQL database
    DATABASE_URL = "postgresql+psycopg2://postgres:pAlcacer9!@localhost:5432/stockfetcher"
    engine = create_engine(DATABASE_URL)

    # Write the DataFrame to a PostgreSQL table
    df.to_sql('fac_mapping', engine, if_exists='replace', index=False)
    logger.info('Successfully updated FAC > GAAP mappings.')

    print(df)