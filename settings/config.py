from typing import Optional
from dataclasses import dataclass as _dataclass


def _config(cls):
	# Editable by calling
	cls.__call__ = cls.__init__
	# Return instance
	return cls()



@_config
@_dataclass
class values:
	app_name: str
	custom_dir: Optional[str] = None

	@property
	def app_name(self):
		if hasattr(self, '_app_name'):
			return self._app_name
		else:
			raise NotSetupError

	@app_name.setter
	def app_name(self, value: str):
		setattr(self, '_app_name', value)


setup = values






class NotSetupError(BaseException):
	"""Called when no app name has been set up"""

	def __init__(self):
		super().__init__("You haven't set your app name "
		                 "(required for deciding the config directory and other things). "
		                 "Call setup() with the name.")
