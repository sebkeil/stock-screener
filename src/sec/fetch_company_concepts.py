'''
Accounting items we need for DCF:

DIVIDENS:
    - PaymentsOfDividends
    - PaymentsOfDividendsCommonStock
    - CommonStockDividendsPerShareCashPaid
    - CommonStockDividendsPerShareDeclared


FREE CASH FLOW
- Total Cash Flows From Operating Activities: NetCashProvidedByUsedInOperatingActivities
    (-) Capital Expenditures
    (+) Net Borrowings


INCOME STATEMENT
    - Revenue
    - CostOfRevenue
    - CostOfGoodsAndServicesSold
    - Gross Margin = (Revenue - CostOfRevenue)/Revenue





'''
import pandas as pd
import requests
from sqlalchemy import create_engine
from logger import logger

CIK = '0000936468'
CONCEPT = 'CostOfGoodsAndServicesSold'


if __name__ == '__main__':

    headers = {
        'User-Agent': 'basti.keil@hotmail.de'
    }

    response = requests.get(f'https://data.sec.gov/api/xbrl/companyconcept/CIK{CIK}/us-gaap/{CONCEPT}.json',
                            headers=headers)

    response_json = response.json()
    revenue_items = response_json['units']['USD']       # extract all revenue items as list of dict

    df = pd.DataFrame(revenue_items)

    df['cik'] = CIK
    df.rename({'val': 'amount', 'fy': 'year', 'fp': 'period'}, axis=1, inplace=True)

    # Create a connection to the PostgreSQL database
    DATABASE_URL = "postgresql+psycopg2://postgres:pAlcacer9!@localhost:5432/stockfetcher"
    engine = create_engine(DATABASE_URL)

    # Write the DataFrame to a PostgreSQL table
    df.to_sql('cost_of_revenue', engine, if_exists='replace', index=False)
    logger.info(f'Successfully updated {CONCEPT}.')



