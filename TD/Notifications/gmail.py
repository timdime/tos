# Importing libraries 
import imaplib, email, re
# from config.credentials import email_address, password2

class TDSecurityCode():

	def __init__(self):

		# Importing libraries 

		user = 'email_address@gmail.com'
		password = #
		imap_url = 'imap.gmail.com'

		# Function to search for a key value pair 
		def search(key, value, con): 
			result, data = con.search(None, key, '"{}"'.format(value)) 
			return data 

		# Function to get the list of emails under this label 
		def get_emails(result_bytes): 
			msgs = [] # all the email data are pushed inside an array 
			for num in result_bytes[0].split(): 
				typ, data = con.fetch(num, '(RFC822)') 
				msgs.append(data) 

			return msgs 

		# this is done to make SSL connnection with GMAIL 
		con = imaplib.IMAP4_SSL(imap_url) 

		# logging the user in 
		con.login(user, password) 

		# calling function to check for email under this label 
		con.select('Inbox') 

		msgs = get_emails(search('FROM', 'XXXXXXXX@txt.voice.google.com', con)) # to get google voice text message to email

		# Uncomment this to see what actually comes as data 
		# print(msgs) 


		# Finding the required content from our msgs 
		# User can make custom changes in this part to 
		# fetch the required content he / she needs 

		# printing them by the order they are displayed in your gmail 
		for msg in msgs[::-1]: 
			for sent in msg: 
				if type(sent) is tuple: 

					# encoding set as utf-8 
					content = str(sent[1], 'utf-8') 
					data = str(content) 

					# Handling errors related to unicodenecode 
					try: 
						indexstart = data.find("ltr") 
						data2 = data[indexstart + 5: len(data)] 
						indexend = data2.find("</div>") 

						# printtng the required content which we need 
						# to extract from our email i.e our body 
						# print(data2[0: indexend]) 
						self.td_security_code = re.search('TD Ameritrade: Your Security Code is (\\d+)', str(msg)).group(1)
						return
					except UnicodeEncodeError as e: 
						pass

TDSecurityCode()
