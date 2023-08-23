import requests
import pandas as pd


CIK = '0000936468'

headers = {
    'User-Agent': 'basti.keil@hotmail.de'
}


response = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{CIK}.json',
                        headers=headers)

print(response.json())


