'''
Run CompanyConceptFetcher

Available concepts:
    - Revenues
'''

from src.sec.fetcher import CompanyConceptFetcher


if __name__ == '__main__':
    MSFT_CIK = '0000789019'
    CONCEPT = 'Revenues'
    fetcher = CompanyConceptFetcher(MSFT_CIK, CONCEPT)
    fetcher.fetch()

