import appdirs, os

from .config import values



def get():
	"""Return where the config values are being stored"""
	if isinstance(values.custom_dir, str):
		return values.custom_dir
	else:
		# noinspection PyTypeChecker
		return appdirs.user_config_dir(values.app_name, False)


