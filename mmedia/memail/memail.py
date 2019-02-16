import email, smtplib, ssl
from .. import config
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail( subject, body, to="", filename=None):
	# Create a multipart message and set headers
	message = MIMEMultipart()
	message["From"] = 'bot@mmediagroup.fr'
	message["To"] = to or config.settings['email']['admin_email_address']
	message["Subject"] = subject

	body += "\n\nRegards,\nBot\n\n\nPlease don't reply to this email, it was generated automatically.\n"

	# Add body to email
	message.attach(MIMEText(body, "plain"))

	if filename != None:
		# Open PDF file in binary mode
		with open(filename, "rb") as attachment:
			# Add file as application/octet-stream
			# Email client can usually download this automatically as attachment
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())

		# Encode file in ASCII characters to send by email
		encoders.encode_base64(part)

		# Add header as key/value pair to attachment part
		part.add_header(
			"Content-Disposition",
			"attachment; filename= {}".format(filename),
		)

		# Add attachment to message and convert message to string
		message.attach(part)

	text = message.as_string()

	# Log in to server using secure context and send email
	context = ssl.create_default_context()
	server = smtplib.SMTP(config.settings['email']['smtp'], 587)
	server.starttls(context=context) # Secure the connection
	server.login(config.settings['email']['account'], config.settings['email']['password'])
	server.sendmail('bot@mmediagroup.fr', [to, config.settings['email']['admin_email_address']], text)
	print("Email sent \n")