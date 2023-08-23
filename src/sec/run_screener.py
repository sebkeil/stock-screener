import requests
import pandas as pd


headers = {
    'User-Agent': 'basti.keil@hotmail.de'
}

company_tickers = requests.get('https://www.sec.gov/files/company_tickers.json',
                               headers=headers)

company_data = pd.DataFrame.from_dict(company_tickers.json(), orient='index')

company_data['cik_str'] = company_data['cik_str'].astype(str).str.zfill(10)

print(company_data)

test_cik = company_data.iloc[0, 0]

submission_hist = requests.get(f'https://data.sec.gov/submissions/CIK{test_cik}.json',
                               headers=headers)

print(submission_hist)

# extract all recent forms
all_forms = pd.DataFrame.from_dict(submission_hist.json()['filings']['recent'])

print(all_forms)


company_facts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{test_cik}.json',
                             headers=headers)

print(company_facts.json())