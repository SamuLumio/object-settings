import appdirs
from dataclasses import dataclass as _dataclass


def _instance(cls):
	# Editable by calling
	cls.__call__ = cls.__init__
	# Return instance
	return cls()



@_instance
@_dataclass
class values:
	"""Call this to configure the library to better suit your app.
	Only app_name is required, all other values are optional."""

	app_name: str = None
	"""The name/id of your app - used to generate paths for config files and keys for environment variables 
	(this is the only required option)"""

	custom_dir: str | None = None
	"""Custom directory to store config files in instead of the one generated with app_name"""

	use_env: bool = True
	"""Allow loading setting values from environment variables 
	(using standard form of capitalized-underscored APPNAME_SETTING_NAME)"""


	def __getattribute__(self, item):
		value = super().__getattribute__(item)
		if item == 'app_name' and value is None:
			raise NotSetupError
		else:
			return value


# Aliases because the class serves as both of these things
setup = values
config = values




def get_dir():
	"""Return where the config values are being stored"""
	if isinstance(config.custom_dir, str):
		return config.custom_dir
	else:
		# noinspection PyTypeChecker
		return appdirs.user_config_dir(config.app_name, False)






class NotSetupError(BaseException):
	"""Called when no app name has been set up"""

	def __init__(self):
		super().__init__("You haven't set your app name "
		                 "(required for deciding the config directory and other things). "
		                 "Call setup() with the name.")
