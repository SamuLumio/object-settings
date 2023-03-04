import appdirs
from typing import Optional
from dataclasses import dataclass as _dataclass


def _instance(cls):
	# Editable by calling
	cls.__call__ = cls.__init__
	# Return instance
	return cls()



@_instance
@_dataclass
class values:
	app_name: str = None
	custom_dir: Optional[str] = None

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
