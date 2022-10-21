import appdirs, os


_dir: str | None = None


def setup(app_name, custom_dir: str = None):
	"""Creates the config dir with your app name. Required to use the package."""
	if isinstance(custom_dir, str):
		config_dir = custom_dir
	else:
		# noinspection PyTypeChecker
		config_dir = appdirs.user_config_dir(app_name, False)
	os.makedirs(config_dir, exist_ok=True)
	global _dir
	_dir = config_dir


def get():
	"""Return where the config values are being stored"""
	if isinstance(_dir, str):
		return _dir
	else:
		raise NotSetupError


class NotSetupError(BaseException):
	"""Called when no app name has been set up"""
	def __init__(self):
		super().__init__("You haven't set your app name (required for deciding the config file directory). "
						 "Call setup() with the name.")
