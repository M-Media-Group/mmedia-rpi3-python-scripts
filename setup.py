from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from subprocess import check_call

# Project basic data variables
__project__ = "M_Media"
__version__ = "0.0.3"
__description__ = "a Python module set for M Media"
__packages__ = ["mmedia", "mmedia.bot", "mmedia.instagram", "mmedia.memail"]

class PostInstallCommand(install):
	"""Post-installation for installation mode."""
	def run(self):
		#check_call("pip3 uninstall --yes instapy-chromedriver".split())
		#check_call("pip3 install instapy-chromedriver==2.36.post0".split())
		#check_call("export PATH=~/.local/bin:$PATH".split())

		install.run(self)

class PostDevelopCommand(develop):
	"""Post-installation for installation mode."""
	def run(self):
		# PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION

		develop.run(self)

setup(
	# Basic setup data
	name = __project__,
	version = __version__,
	description = __description__,
	packages = __packages__,

	# This makes the console commands possible
	entry_points="""
	[console_scripts]
	boot-checkin = mmedia.bot.boot_checkin:sendEmail
	m-insta-report = mmedia.instagram.generateReport:sendEmail
	m-install = mmedia.install:install
	""",

	# Install the dependencies
	install_requires=[
		  'schedule', 'xlsxwriter'
	  ],

	# Trigger post install scripts
	cmdclass={
		'install': PostInstallCommand,
		'develop': PostDevelopCommand,
	}
)
