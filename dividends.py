'''

Candidates for scraping:
- https://dividendhistory.org/payout/MMM/
- https://www.nasdaq.com/market-activity/stocks/aapl/dividend-history
'''


import requests


response = requests.get('https://dividendhistory.org/payout/MMM/')

print(response)