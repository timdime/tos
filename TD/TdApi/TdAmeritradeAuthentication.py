import time
import datetime
import json
import urllib
import requests
import dateutil.parser
import os
from splinter import Browser
from Notifications.gmail import TDSecurityCode

# https://developer.tdameritrade.com/apis

class RefreshToken(object):

	def __init__(self, TimeObject):

		self.client_id = TimeObject.client_id
		self.refresh_token = TimeObject.refresh_token

		endpoint = 'https://api.tdameritrade.com/v1/oauth2/token'
		headers = {'Content-Type': 'application/x-www-form-urlencoded'}
		data = {'grant_type': 'refresh_token',
				'refresh_token': self.refresh_token,
				'client_id': self.client_id}

		resp = requests.post(endpoint, headers=headers, data=data)

		if resp.status_code != 200:
			raise Exception('Could not authenticate!')
		else:
			print("Access Token Refreshed.  This occurs every 29 minutes to avoid 30 minute expiration.")
	    
		decoded_content = resp.json()

		self.access_token = decoded_content['access_token']


class TDAuthenticate(object):

	def __init__(self, client_id, password, account_number, redirect_uri):
		self.client_id = client_id
		self.account_number = account_number
		self.password = password
		self.redirect_uri = redirect_uri
		self.access_code = None
		self.access_token = None
		self.credentials = None
		self.login_encoded = None
		self.userPrincipalsResponse = None

	def get_access_code(self):
		executable_path = {'executable_path': './resources/chromedriver'}

		browser = Browser('chrome', headless=True, **executable_path)

		method = 'GET'
		url = 'https://auth.tdameritrade.com/auth?'
		client_code = self.client_id + '@AMER.OAUTHAP'
		payload = { 'response_type': 'code',
					'redirect_uri': self.redirect_uri,
					'client_id': client_code}

		p = requests.Request(method, url, params = payload).prepare()
		myurl = p.url

		browser.visit(myurl)

		payload = {'username': self.account_number,
					'password': self.password}

		browser.find_by_id("username").first.fill(payload['username'])
		browser.find_by_id("password").first.fill(payload['password'])
		browser.find_by_id("accept").first.click()
		time.sleep(1)
		browser.find_by_id("accept").first.click()

		time.sleep(5)
		td_security_code=TDSecurityCode()
		browser.find_by_id("smscode").first.fill(td_security_code.td_security_code)

		browser.find_by_id("accept").first.click()
		browser.find_by_id("accept").first.click()

		new_url = browser.url

		self.access_code = urllib.parse.unquote(new_url.split('code=')[1])

		browser.quit()

	def get_access_token(self):

		# https://developer.tdameritrade.com/authentication/apis/post/token-0

		headers = {'Content-Type':"application/x-www-form-urlencoded"}

		payload = {'grant_type':'authorization_code',
					'access_type':'offline',
					'code':self.access_code,
					'client_id':self.client_id,
					'redirect_uri':self.redirect_uri}

		authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers = headers, data = payload)

		decoded_content = authReply.json()

		self.refresh_token = decoded_content['refresh_token']
		self.access_token = decoded_content['access_token']


	def get_credentials(self):

		# https://developer.tdameritrade.com/user-principal/apis/get/userprincipals-0

		endpoint = 'https://api.tdameritrade.com/v1/userprincipals'
		headers = {'Authorization': "Bearer {}".format(self.access_token)}

		params = {'fields':'streamerSubscriptionKeys,streamerConnectionInfo'}

		content = requests.get(url = endpoint, params = params, headers = headers)

		self.userPrincipalsResponse = content.json()

		tokenTimeStamp = self.userPrincipalsResponse['streamerInfo']['tokenTimestamp']
		date = dateutil.parser.parse(tokenTimeStamp, ignoretz = True)
		tokenTimeStampAsMs = unix_time_millis(date)

		self.credentials = {'userid':self.userPrincipalsResponse['accounts'][0]['accountId'],
			'token':self.userPrincipalsResponse['streamerInfo']['token'],
			'company':self.userPrincipalsResponse['accounts'][0]['company'],
			'segment':self.userPrincipalsResponse['accounts'][0]['segment'],
			'cddomain':self.userPrincipalsResponse['accounts'][0]['accountCdDomainId'],
			'usergroup':self.userPrincipalsResponse['streamerInfo']['userGroup'],
			'accesslevel':self.userPrincipalsResponse['streamerInfo']['accessLevel'],
			'authorized':'Y',
			'timestamp':int(tokenTimeStampAsMs),
			'appId':self.userPrincipalsResponse['streamerInfo']['appId'],
			'acl':self.userPrincipalsResponse['streamerInfo']['acl']}

	def login(self):

		login_request = {'requests': [{"service": "ADMIN",
									  "command": "LOGIN",
									  "requestid": "1",
									  "qoslevel": "0",
									  "account": self.userPrincipalsResponse['accounts'][0]['accountId'],
									  "source": self.userPrincipalsResponse['streamerInfo']['appId'],
									  "parameters": {"credential": urllib.parse.urlencode(self.credentials),
									  				 "token": self.userPrincipalsResponse['streamerInfo']['token'],
									  				 "version": "1.0"}}]}

		self.login_encoded = json.dumps(login_request)

	def authentication(self):

			self.get_access_code()
			self.get_access_token()
			self.get_credentials()
			self.login()

def unix_time_millis(dt):
	epoch = datetime.datetime.utcfromtimestamp(0)
	return (dt - epoch).total_seconds() * 1000.0



