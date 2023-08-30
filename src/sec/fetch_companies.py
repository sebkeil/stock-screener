'''
Fetches all the companies listed with the SEC and stores them in our 'companies' table
'''

import requests
import pandas as pd
from sqlalchemy import create_engine
from logger import logger
import psycopg2
import settings
from utils.db import bulk_insert_on_duplicate_update




if __name__ == '__main__':

    company_tickers = requests.get('https://www.sec.gov/files/company_tickers.json',
                                   headers=settings.sec_header)

    company_data = pd.DataFrame.from_dict(company_tickers.json(), orient='index')

    company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)
    company_data.rename({'cik_str': 'cik',
                         'title': 'name'},
                        axis=1, inplace=True)

    # Create a connection to the PostgreSQL database
    #DATABASE_URL = "postgresql+psycopg2://postgres:pAlcacer9!@localhost:5432/stockfetcher"
    #engine = create_engine(DATABASE_URL)

    CONNECTION_STRING = "dbname=stockfetcher user=postgres password=pAlcacer9! host=localhost port=5432"

    bulk_insert_on_duplicate_update(company_data, 'companies', ['ticker', 'cik'], CONNECTION_STRING)
    
    logger.info('Successfully refreshed companies.')
    # Write the DataFrame to a PostgreSQL table
    #company_data.to_sql('companies', engine, if_exists='replace', index=False)
    #logger.info('Successfully updated companies.')




