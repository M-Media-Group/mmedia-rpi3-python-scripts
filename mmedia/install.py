import pkg_resources
import yaml
#from . import config

def install():
	#smtp = config.settings['email_password'] or "email-smtp.eu-west-1.amazonaws.com";

	data = dict(
		email = dict(
			admin_email_address = input('Admin email address: '),
	        account = input('Email account: ') ,
	        password = input('Email pass: ') ,
	        from_email_address = input('From email address: '),
	        smtp = input('SMTP server: ') or "email-smtp.eu-west-1.amazonaws.com",
	    ),
	    device = dict(
	        id = input('Pi ID: '),
	    ),
	    client = dict(
	    	email = input('Client email: '),
	    )
	)

	with open(pkg_resources.resource_filename(__name__, "settings.yml"), 'w+') as outfile:
	    yaml.dump(data, outfile, default_flow_style=False)