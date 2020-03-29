import requests
import json
from config.credentials import account_id

class CancelOrder():

	def __init__(self, accountId, access_token, orderId):

		self.accountId = accountId
		self.orderId = orderId
		self.access_token = access_token

		endpoint = 'https://api.tdameritrade.com/v1/accounts/{accountId}/orders/{orderId}'.format(self.accountId, self.orderId)
		headers = {'Authorization': "Bearer {}".format(self.access_token)}

		content = requests.get(url = endpoint, headers = headers, verify=False)

		self.cancelOrderResponse = content.json()

class GetOrder():

	def __init__(self, accountId, access_token, orderId):

		self.accountId = accountId
		self.orderId = orderId
		self.access_token = access_token

		endpoint = 'https://api.tdameritrade.com/v1/accounts/{accountId}/orders/{orderId}'.format(self.accountId, self.orderId)
		headers = {'Authorization': "Bearer {}".format(self.access_token)}

		content = requests.get(url = endpoint, headers = headers, verify=False)

		self.getOrderResponse = content.json()

class GetOrdersByQuery():

	def __init__(self, accountId, access_token):

		self.accountId = accountId
		self.access_token = access_token

		endpoint = 'https://api.tdameritrade.com/v1/orders'
		headers = {'Authorization': "Bearer {}".format(self.access_token)}

		params = {'accountId': self.accountId,
				  'status': "WORKING"
				 }

		content = requests.get(url = endpoint, params=params, headers = headers, verify=False)

		self.getOrdersByQueryResponse = content.json()


class PlaceStrategyOrder():

	def __init__(self, tradeDictionary, access_token):

		self.tradeDictionary = tradeDictionary
		self.access_token = access_token
		
		exit_side = ""
		if self.tradeDictionary['side'] == "SELL":
			self.tradeDictionary['side'] = "SELL_SHORT"
			exit_side = "BUY"
		elif self.tradeDictionary['side'] == "BUY":
			exit_side = "SELL"

		endpoint = 'https://api.tdameritrade.com/v1/accounts/{}/orders'.format(account_id)
		
		headers = {'Authorization': "Bearer {}".format(self.access_token),
					"Content-Type": "application/json"}

		payload = {
					  "orderStrategyType": "TRIGGER",
					  "session": "NORMAL",
					  "duration": "FILL_OR_KILL",
					  "orderType": "LIMIT",
					  "price": "{}".format(self.tradeDictionary['entry_price']),
					  "orderLegCollection": [
					    {
					      "instruction": "{}".format(self.tradeDictionary['side']),
					      "quantity": "{}".format(self.tradeDictionary['quantity']),
					      "instrument": {
					        "assetType": "EQUITY",
					        "symbol": "{}".format(self.tradeDictionary['symbol'])
					      }
					    }
					  ],
					  "childOrderStrategies": [
					    {
					      "orderType": "TRAILING_STOP",
					      "stopPriceLinkBasis": "LAST",
    					  "stopPriceLinkType": "VALUE",
    					  # "stopPriceOffset": "{}".format(self.tradeDictionary['trailing_stop']),
    					  "stopPriceOffset": ".10",
					      "session": "NORMAL",
					      "duration": "DAY",
					      "orderStrategyType": "SINGLE",
					      "orderLegCollection": [
					        {
					          "instruction": "{}".format(exit_side),
					          "quantity": "{}".format(self.tradeDictionary['quantity']),
					          "instrument": {
					            "symbol": "{}".format(self.tradeDictionary['symbol']),
					            "assetType": "EQUITY"
					          }
					        }
					      ]
					    }
					  ]
					}


		# payload = {
		# 			  "orderStrategyType": "TRIGGER",
		# 			  "session": "NORMAL",
		# 			  "duration": "FILL_OR_KILL",
		# 			  "orderType": "LIMIT",
		# 			  "price": "{}".format(self.tradeDictionary['entry_price']),
		# 			  "orderLegCollection": [
		# 			    {
		# 			      "instruction": "{}".format(self.tradeDictionary['side']),
		# 			      "quantity": "{}".format(self.tradeDictionary['quantity']),
		# 			      "instrument": {
		# 			        "assetType": "EQUITY",
		# 			        "symbol": "{}".format(self.tradeDictionary['symbol'])
		# 			      }
		# 			    }
		# 			  ],
		# 			  "childOrderStrategies": [
		# 			    {
		# 			      "orderStrategyType": "OCO",
		# 			      "childOrderStrategies": [
		# 			        {
		# 			          "orderStrategyType": "SINGLE",
		# 			          "session": "NORMAL",
		# 			          "duration": "DAY",
		# 			          "orderType": "LIMIT",
		# 			          "price": "{}".format(self.tradeDictionary['exit_price']),
		# 			          "orderLegCollection": [
		# 			            {
		# 			              "instruction": "{}".format(exit_side),
		# 			              "quantity": "{}".format(self.tradeDictionary['quantity']),
		# 			              "instrument": {
		# 			                "assetType": "EQUITY",
		# 			                "symbol": "{}".format(self.tradeDictionary['symbol'])
		# 			              }
		# 			            }
		# 			          ]
		# 			        },
		# 			        {
		# 			          "orderStrategyType": "SINGLE",
		# 			          "session": "NORMAL",
		# 			          "duration": "DAY",
		# 			          "orderType": "STOP",
		# 			          "stopPrice": "{}".format(self.tradeDictionary['stop_trigger']),
		# 			          "stopType": 'LAST',
		# 			          # "price": "{}".format(self.tradeDictionary['stop_price']),
		# 			          "orderLegCollection": [
		# 			            {
		# 			              "instruction": "{}".format(exit_side),
		# 			              "quantity": "{}".format(self.tradeDictionary['quantity']),
		# 			              "instrument": {
		# 			                "assetType": "EQUITY",
		# 			                "symbol": "{}".format(self.tradeDictionary['symbol'])
		# 			              }
		# 			            }
		# 			          ]
		# 			        }
		# 			      ]
		# 			    }
		# 			  ]
		# 			}

		print("\n\nurl: {}".format(endpoint))
		print("\n\nheaders: \n{}".format(headers))			
		print("\n\npayload: \n{}\n\n\n".format(payload))

		content = requests.post(url=endpoint, json=payload, headers=headers, verify=False)

		print(content.content.decode())

		if content.status_code == 200:
			print("\nStatus 200- Trade Placed Successfully!\n")
		
		self.placeStrategyOrderResponse = content.status_code

# class PlaceOrder():

# 	def __init__(self, accountId, access_token, symbol, entryPrice, side):

# 		self.symbol = symbol
# 		self.entryPrice = entryPrice
# 		self.side = side
# 		self.accountId = accountId
# 		self.access_token = access_token

# 		endpoint = 'https://api.tdameritrade.com/v1/accounts/{accountId}/orders'.format(self.accountId)	
# 		headers = {'Authorization': "Bearer {}".format(self.access_token)}
		
# 		params = {'accountId': self.accountId,
# 				  'status': "WORKING"
# 				 }

# 		content = requests.get(url = endpoint, params=params, headers = headers, verify=False)

# 		self.placeOrderResponse = content.json()

