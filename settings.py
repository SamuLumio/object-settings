"""
Simple object-oriented config library, where your settings are objects.

Their values get saved to a standard config location, depending on the os (uses `appdirs` package for paths).
The file is automatically written and read, so you don't have to worry about it.

Just remember to call setup() with your app name before defining any settings.
"""

import configparser
import typing
import appdirs
import os







_path: typing.Union[str, None] = None
"""Path of the config file all settings will be saved to / read from"""


def setup(app_name):
	"""Creates the config path with your app name. Required to use the package."""
	config_dir = appdirs.user_config_dir(app_name)
	os.makedirs(config_dir, exist_ok=True)
	global _path
	_path = os.path.join(config_dir, 'settings.cfg')


class _NotSetupError(BaseException):
	"""Called when no app name has been set up"""
	def __init__(self):
		super().__init__("You haven't set your app name (required for deciding the config file path)."
		                 "Call setup() with the name.")










class _Setting:
	"""Base setting class"""
	def __init__(self, name: str, default):
		self.name = name
		self.default = default
		self.section = 'SETTINGS'

		# Make sure that file path is set
		if _path is None:
			raise _NotSetupError

		# Initialize lower-level config parser
		self._parser = configparser.ConfigParser()

		# Make parser preserve case
		self._parser.optionxform = str

		# Make sure that file/section/option exists
		for i in range(3):
			try:
				self.get()
				break
			except configparser.NoSectionError:
				self._parser.add_section(self.section)
			except configparser.NoOptionError:
				self._parser.set(self.section, self.name, str(self.default))
				with open(_path, 'w') as f:
					self._parser.write(f)


	def get(self):
		self._parser.read(_path)
		return self._parser.get(self.section, self.name)

	def set(self, new_value):
		self._parser.read(_path)
		self._parser.set(self.section, self.name, str(new_value))

		with open(_path, 'w') as f:
			self._parser.write(f)


	@property
	def value(self):
		return self.get()

	@value.setter
	def value(self, new_value):
		self.set(new_value)


	def __repr__(self):
		return f"{self.name}: {self.value}"

	def __iter__(self):
		return self.value.__iter__()






class Toggle(_Setting):
	"""A boolean True/False"""
	def __init__(self, name, default: bool):
		super().__init__(name, default)

	def get(self) -> bool:
		self._parser.read(_path)
		return self._parser.getboolean(self.section, self.name)

	def toggle(self):
		self.set(not self.get())


	def __bool__(self):
		return self.value





class Choice(_Setting):
	"""Choose an option (str) from a list"""
	def __init__(self, name, options: typing.Iterable[str], default: str):
		super().__init__(name, default)
		self.options = options

	def set(self, new_value: str):
		if new_value in self.options:
			super().set(new_value)
		else:
			raise ValueError(f"New value {new_value} not in options ({self.options})")





class Multichoice(_Setting):
	"""Choose multiple options (str) from a list"""
	def __init__(self, name, options: typing.Iterable[str], default_choices: typing.Iterable[str]):
		super().__init__(name, default_choices)
		self.options = options

	def get(self):
		return eval(super().get())

	def set(self, new_value: typing.Iterable[str]):
		for value in new_value:
			if value not in self.options:
				raise ValueError(f"New value {new_value} not in options ({self.options})")

		super().set(new_value)


	def append(self, item: str):
		value = self.get()
		value.append(item)
		self.set(value)

	def remove(self, item: str):
		value = self.get()
		value.remove(item)
		self.set(value)





class Text(_Setting):
	"""Normal text"""
	def __init__(self, name, default: str):
		super().__init__(name, default)


class Path(_Setting):
	"""A file path. Functionally indifferent from Text, used for seperation eg. in a GUI for a file picker."""
	def __init__(self, name, default: str):
		super().__init__(name, default)




class Number(_Setting):
	"""A number (int) that can be incremented and decremented"""
	def __init__(self, name, default: int):
		super().__init__(name, default)

	def get(self):
		return int(super().get())

	def increment(self):
		self.set(self.get() + 1)

	def decrement(self):
		self.set(self.get() - 1)
