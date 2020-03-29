import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.credentials import password2, email_address

class SendEmail(object):

	def __init__(self, subject, body):

		self.subject = subject
		self.body = body
		self.email_address = email_address
		self.password = password2

		#Setup the MIME
		message = MIMEMultipart()
		message['From'] = self.email_address
		message['To'] = self.email_address
		message['Subject'] = self.subject   #The subject line

		#The body and the attachments for the mail
		message.attach(MIMEText(self.body, 'text'))

		#Create SMTP session for sending the mail
		session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
		session.starttls() #enable security
		session.login(self.email_address, self.password) #login with mail_id and password
		text = message.as_string()
		session.sendmail(self.email_address, self.email_address, text)
		session.quit()
