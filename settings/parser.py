import configparser
import os.path
import typing


class ConfigFile:
	"""Controller/parser for a config file.
	Can technically be used by itself without the rest of the library, if you want dict-style settings instead."""
	def __init__(self, path: str | typing.Callable[[], str], title="Settings"):
		super().__init__()
		self._path = path
		self.title = title

		# Initialize lower-level config parser
		self._parser = configparser.ConfigParser()
		self._parser.optionxform = str  # For preserve case

		# Make sure that section exists
		if self.title not in self._parser.sections():
			self._parser.add_section(self.title)

	@property
	def path(self):
		if callable(self._path):  # For the default section, so it can be defined without knowing the dir yet
			return str(self._path())
		else:
			return str(self._path)


	def reload(self):
		self._parser.read(self.path)

	def _write(self):
		os.makedirs(os.path.dirname(self.path), exist_ok=True)
		with open(self.path, 'w') as f:
			self._parser.write(f)



	def get(self, option: str, type: typing.Type[str | int | float | bool | list]):
		self.reload()
		special_functions = {
			str: self._parser.get,
			int: self._parser.getint,
			float: self._parser.getfloat,
			bool: self._parser.getboolean,
			list: lambda *args: self._parser.get(*args).strip("['").strip("']").split("', '")
		}
		function = special_functions[type]
		return function(self.title, option)


	def set(self, option: str, value):
		self._parser.set(self.title, option, str(value))
		self._write()


	def remove(self, option: str):
		self._parser.remove_option(self.title, option)
		self._write()


	def keys(self):
		self.reload()
		return self._parser.options(self.title)
