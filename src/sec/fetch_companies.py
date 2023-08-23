'''
Fetches all the companies listed with the SEC and stores them in our 'companies' table
'''

import requests
import pandas as pd
from sqlalchemy import create_engine
from logger import logger
import psycopg2
import settings

headers = {
    'User-Agent': 'basti.keil@hotmail.de'
}

if __name__ == '__main__':

    company_tickers = requests.get('https://www.sec.gov/files/company_tickers.json',
                                   headers=headers)

    company_data = pd.DataFrame.from_dict(company_tickers.json(), orient='index')

    company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)
    company_data.rename({'cik_str': 'cik'}, axis=1, inplace=True)

    # Create a connection to the PostgreSQL database
    DATABASE_URL = "postgresql+psycopg2://postgres:pAlcacer9!@localhost:5432/stockfetcher"
    engine = create_engine(DATABASE_URL)

    # Write the DataFrame to a PostgreSQL table
    company_data.to_sql('companies', engine, if_exists='replace', index=False)
    logger.info('Successfully updated companies.')




