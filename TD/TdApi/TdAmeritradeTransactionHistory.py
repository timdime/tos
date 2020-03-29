import requests
import json
from datetime import datetime

# https://developer.tdameritrade.com/transaction-history/apis/get/accounts/%7BaccountId%7D/transactions-0

class GetTransactions():

	def __init__(self, access_token, accountId):

		endpoint = 'https://api.tdameritrade.com/v1/accounts/{accountId}/transactions'.format(accountId=accountId)
		headers = {'Authorization': "Bearer {}".format(access_token)}

		params = {'type': 'TRADE',
				  'startDate': datetime.today().strftime('%Y-%m-%d')}

		content = requests.get(url = endpoint, params=params, headers = headers)

		self.getTransactionsResponse = content.json()
