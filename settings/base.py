import os

from . import dir, parser




class Section:
	"""A group of settings that is also represented by one file.
	Usage of these is optional, settings defined without sections will use the default one."""
	def __init__(self, name: str):
		self.name = name
		self.settings = []
		self.file = parser.ConfigFile(self.get_path, title=self.name)
		all_sections.append(self)

	def get_path(self):
		return os.path.join(dir.get(), self.name + '.cfg')



all_sections: list[Section] = []
default_section = Section('Settings')




class Setting:
	"""Base setting class"""
	def __init__(self, datatype, name: str, default, section: Section = default_section):
		self.datatype = datatype
		self.name = name
		self.default = default
		self.section = section

		# if self.section == default_section and type(default_section) != section:
		# 	_setup_default_section()
		
		# self.section.add(self)
		if self not in self.section.settings:
			self.section.settings.append(self)

		# Make sure that file/section/option exists
		if self.name not in self.section.file.keys():
			self.set(self.default)


	def validate(self, value) -> bool:
		return type(value) == self.datatype
		# Expanded within each setting type



	def get(self):
		"""Return stored value, or the default if invalid or missing"""
		value = self.section.file.get(self.name, self.datatype)
		if self.validate(value):
			return value
		else:
			return self.default

	def set(self, new_value):
		valid = self.validate(new_value)
		if not valid:
			raise ValueError(f"New setting value {new_value} is invalid")
		self.section.file.set(self.name, new_value)


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


	def __eq__(self, other):
		if isinstance(other, Setting):
			return (other.name == self.name) and (other.section == self.section)

