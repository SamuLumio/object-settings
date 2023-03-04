import os, threading, typing

from . import parser, get_dir




class Section:
	"""A group of settings that is also represented by one file.
	Usage of these is optional, settings defined without sections will use the default one."""
	def __init__(self, name: str):
		self.name = name
		self.settings = []
		self.file = parser.ConfigFile(self.get_path, title=self.name)
		all_sections.append(self)

	def get_path(self):
		"""Return the file the values are stored in"""
		return os.path.join(get_dir(), self.name + '.cfg')



all_sections: list[Section] = []
default_section = Section('Settings')




class Setting:
	"""Base setting class - can be effectively subclassed to create custom setting types"""
	def __init__(self, datatype, name: str, default, section: Section = default_section):
		self.datatype = datatype
		self.name = name
		self.default = default
		self.section = section
		self.listeners = []

		if self not in self.section.settings:
			self.section.settings.append(self)

		# Make sure that option always exists in file, so it can be easily edited from there
		if self.name not in self.section.file.keys():
			self.set(self.default)


	def add_listener(self, function: typing.Callable[[], None]):
		"""Add a function to be called when the setting is changed"""
		if function not in self.listeners:
			self.listeners.append(function)


	def validate(self, value) -> bool:
		"""Check if value is valid and can be set for this setting"""
		return type(value) == self.datatype
		# Expanded within each setting type

	def check_validate(self, value):
		"""Call validate() and raise ValueError if value is not valid"""
		if not self.validate(value):
			raise ValueError


	def get(self):
		"""Return stored value, or the default if invalid or missing"""
		try:
			value = self.section.file.get(self.name, self.datatype)
			self.check_validate(value)
			return value
		except:
			return self.default

	def set(self, new_value):
		"""Validate and set a new value. Invalid values will raise a ValueError."""
		valid = self.validate(new_value)
		if not valid:
			raise ValueError(f"New setting value {new_value} is invalid")
		self.section.file.set(self.name, new_value)

		for listener in self.listeners:
			threading.Thread(target=listener, daemon=True).start()


	def reset(self):
		"""Sets the setting back to its default value"""
		self.set(self.default)


	@property
	def value(self):
		"""The stored value - can also be set with this variable"""
		return self.get()

	@value.setter
	def value(self, new_value):
		"""The stored value - can also be set with this variable"""
		self.set(new_value)


	def __repr__(self):
		return f"{self.name}: {self.value}"

	def __iter__(self):
		return self.value.__iter__()


	def __eq__(self, other):
		"""Supports comparing with actual types (and other settings)"""
		if isinstance(other, Setting):
			return (other.name == self.name) and (other.section == self.section)
		elif isinstance(other, self.datatype):
			return self.value == other
