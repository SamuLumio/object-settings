import threading, typing

from . import backend, config




class Section:
	"""A group of settings that is also represented by one config file.
	Usage of these is optional – settings defined without sections will use the default one."""
	def __init__(self, name: str):
		self.name = name
		self.settings = []
		self._storage = None
		self.environment = backend.Environment()
		all_sections.append(self)

	@property
	def storage(self):
		if self._storage is None:
			self._storage = backend.Storage(self.name)
		return self._storage
	
	def is_default(self):
		"""Check if this section is the default section"""
		return self == default_section


all_sections: list[Section] = []




class _DefaultSection(Section):

	@property
	def name(self):
		return config.default_section_name
	
	@name.setter
	def name(self, value):
		pass
	
default_section = _DefaultSection('')





class BaseSetting:
	"""Base setting class - can be safely subclassed to create custom setting types"""
	def __init__(self, datatype, name: str, default, section: Section = default_section):
		self.datatype = datatype
		self.name = name
		self.default = default
		self.section = section
		self.listeners = []

		if self not in self.section.settings:
			self.section.settings.append(self)

		# Make sure that option always exists in file, so it can be easily edited from there
		if not self.section.storage.exists(self.name):
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


	def get(self) -> typing.Any:
		"""Return the set value, or the default if invalid or missing"""
		try:
			if self.set_externally:
				value = self.section.environment.get(self.name, self.datatype)
			else:
				value = self.section.storage.get(self.name, self.datatype)
			self.check_validate(value)
			return value
		except:
			return self.default

	def set(self, new_value):
		"""Validate and set a new value. Invalid values will raise a ValueError."""
		if not self.validate(new_value):
			raise ValueError(f"New setting value {new_value} is invalid")
		self.section.storage.set(self.name, new_value)
		for listener in self.listeners:
			listener()

	@property
	def set_externally(self):
		"""See if the value is set from the environment (like env vars or cli params)"""
		return config.use_environment and self.section.environment.exists(self.name)

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
		if isinstance(other, BaseSetting):
			return (other.name == self.name) and (other.section == self.section)
		elif isinstance(other, self.datatype):
			return self.value == other


Setting = BaseSetting  # for backwards compatibility
