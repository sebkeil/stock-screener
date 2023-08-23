import requests
import pandas as pd

headers = {
    'User-Agent': 'basti.keil@hotmail.de'
}

CIK = '0000936468'

if __name__ == '__main__':
    submission_hist = requests.get(f'https://data.sec.gov/submissions/CIK{CIK}.json',
                                   headers=headers)

    df = pd.DataFrame.from_dict(submission_hist.json(), orient='index')

    print(df)