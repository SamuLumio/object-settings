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
	"""Call this or set attributes to configure the library to better suit your app.
	Only app_name is required, all other values are optional."""

	app_name: str = ""
	"""REQUIRED: The name/id of your app - used to generate paths for config files and keys for environment variables 
	(this is the only required option)"""

	custom_dir: str | None = None
	"""Custom directory to store config files in instead of the one generated with app_name"""

	use_environment: bool = True
	"""Allow loading setting values from the enviroment (like env vars and command line options). \n
	If a setting's value has been set from the environment, it takes priority over any stored configurations, 
	and it can't be changed on runtime. 
	You can still set new values for settings, 
	but they will be saved to storage and the get() method will keep returning the environment value."""

	storage_parsers: list[type[parsers.StorageParserTemplate]] = _field(
		default_factory=parsers.storage_parsers.copy)
	"""Select which storage sources and file formats to get setting values from. 
	By default all builtin ones are selected. \n 
	If you want to implement custom ones, subclass backend.parsers.StorageParserTemplate, 
	implement all the methods, and add your own parser classes to this list."""

	environment_parsers: list[type[parsers.EnvironmentParserTemplate]] = _field(
		default_factory=parsers.environment_parsers.copy)
	"""Select which environment sources to get setting values from (these take priority over the storage parsers). 
	By default all builtin ones are selected. \n 
	If you want to implement custom ones, subclass backend.parsers.EnvironmentParserTemplate, 
	implement all the methods, and add your own parser classes to this list."""



	def __getattribute__(self, item):
		value = super().__getattribute__(item)
		if item == 'app_name' and value == "":
			raise NotSetupError
		else:
			return value


# Aliases because the values class serves as both of these things
setup = values
config = values






class NotSetupError(BaseException):
	"""Called when no app name has been set up"""

	def __init__(self):
		super().__init__("You haven't set your app name "
		                 "(required for deciding the config directory and other things). "
		                 "Call setup() with the name.")
