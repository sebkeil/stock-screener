'''
Contains all the classes for fetching data from the SEC

Main logic:
    -

#toDO:
    - check SalesRevenueServicesNet + SalesRevenueGoodsNet for MSFT Q2 2018, how to reconcile?
'''

from settings import SEC_HEADERS, DB_CONNECTION_STRING
import requests
import psycopg2
from logger import logger
import pandas as pd


class CompanyConceptFetcher:

    def __init__(self, cik, concept):
        self.cik = cik
        self.concept = concept
        self.headers = SEC_HEADERS
        self.db_connection_string = DB_CONNECTION_STRING

    def get_taxonomy_concepts(self):
        # get all the sub-concepts associated with a concept
        with psycopg2.connect(self.db_connection_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT taxonomy_concept FROM concepts "
                               f"WHERE concept = 'fac:{self.concept}';")
                taxonomy_concepts = cursor.fetchall()

        if len(taxonomy_concepts):
            taxonomy_concepts = [tc[0] for tc in taxonomy_concepts]     # unpack tuples
            taxonomy_concepts = [(tc.split(':')[0], tc.split(':')[-1]) for tc in taxonomy_concepts]

            return taxonomy_concepts

        else:
            return None

    def fetch(self):
        taxonomy_concepts = self.get_taxonomy_concepts()
        for taxonomy, taxonomy_concept in taxonomy_concepts:
            logger.info(f'Taxonomy: {taxonomy}, Concept: {taxonomy_concept}')

            if taxonomy_concept == 'RevenueFromContractWithCustomerExcludingAssessedTax':
                print('PAUSE!')

            sec_url = f'https://data.sec.gov/api/xbrl/companyconcept/CIK{self.cik}/{taxonomy}/{taxonomy_concept}.json'
            response = requests.get(sec_url, headers=self.headers)

            if response.status_code == 200:
                response_json = response.json()
                items = response_json['units']['USD']
                df = pd.DataFrame(items)
                print(df)

            elif response.status_code == 403:
                logger.info(f'Company {self.cik} does not associate with concept {taxonomy_concept}')

            else:
                logger.error(f'Received unexpected response code: {response.status_code}')




