import pkg_resources
import yaml
from . import install

try:
	settings = yaml.safe_load(pkg_resources.resource_string(__name__, "settings.yml"))
except:
	install.install()
