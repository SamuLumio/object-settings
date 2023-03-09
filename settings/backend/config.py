from dataclasses import dataclass as _dataclass, field as _field, fields as _fields

from . import parsers


def _instance(cls):
	# Editable by calling
	def update(self, *args, **kwargs):
		field_list = _fields(self)
		fields = {field.name: field for field in field_list}
		for index, arg in enumerate(args):
			field = field_list[index]
			kwargs[field.name] = arg
		for field, value in kwargs.items():
			if field != fields[field].default:
				setattr(self, field, value)
	cls.__call__ = update
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

	use_environment: bool = True
	"""Allow loading setting values from the enviroment
	(like env vars and command line options)"""

	storage_parsers: list[type[parsers.StorageParser]] = _field(
		default_factory=parsers.storage_parsers.copy)

	environment_parsers: list[type[parsers.EnvironmentParser]] = _field(
		default_factory=parsers.environment_parsers.copy)


	def __getattribute__(self, item):
		value = super().__getattribute__(item)
		if item == 'app_name' and value is None:
			raise NotSetupError
		else:
			return value


# Aliases because the class serves as both of these things
setup = values
config = values






class NotSetupError(BaseException):
	"""Called when no app name has been set up"""

	def __init__(self):
		super().__init__("You haven't set your app name "
		                 "(required for deciding the config directory and other things). "
		                 "Call setup() with the name.")
