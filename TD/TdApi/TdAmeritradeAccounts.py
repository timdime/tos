import requests
import json

# https://developer.tdameritrade.com/account-access/apis/get/accounts-0

class GetAccounts():

	def __init__(self, access_token):

		endpoint = 'https://api.tdameritrade.com/v1/accounts/'
		headers = {'Authorization': "Bearer {}".format(access_token)}

		params = {'fields': 'positions,orders'}

		content = requests.get(url = endpoint, params=params, headers = headers)

		self.getAccountsResponse = content.json()
