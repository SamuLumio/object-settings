import configparser
import os.path
import typing


class ConfigFile:
	"""Controller/parser for a config file.
	Can technically be used by itself without the rest of the library, if you want dict-style settings instead."""
	def __init__(self, path: str | typing.Callable[[], str], title="Settings"):
		"""
		Controller/parser for a config file.
		Can technically be used by itself without the rest of the library, if you want dict-style settings instead.

		:param path: Either a path string or a function that returns a path string. File doesn't have to exist in advance.
		:param title: Header to write to the top of the file
		"""
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
		"""Get the path of the file."""
		if callable(self._path):  # For the default section, so it can be defined without knowing the dir yet
			return str(self._path())
		else:
			return str(self._path)


	def reload(self):
		"""Load values from file. If file is invalid it will be ignored and overwritten."""
		try:
			self._parser.read(self.path)
		except:
			self._write()

	def _write(self):
		"""Dump all current values to the file."""
		os.makedirs(os.path.dirname(self.path), exist_ok=True)
		with open(self.path, 'w') as f:
			self._parser.write(f)



	def get(self, option: str, type: typing.Type[str | int | float | bool | list]):
		"""Reload and get value."""
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
		"""Set a value and write to the file."""
		self._parser.set(self.title, option, str(value))
		self._write()


	def remove(self, option: str):
		"""Remove an option (and update the file)."""
		self._parser.remove_option(self.title, option)
		self._write()


	def keys(self):
		"""Return list of all defined options."""
		self.reload()
		return self._parser.options(self.title)
