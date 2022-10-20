import os

from . import dir, parser




class Section:
	"""A group of settings that is also represented by one file.
	Usage of these is optional, settings defined without sections will use the default one."""
	def __init__(self, name: str):
		self.name = name
		self.settings = []
		self.file = parser.ConfigFile(self.get_path)

	def get_path(self):
		return os.path.join(dir.get(), self.name + '.cfg')


	# def add(self, *settings):
	# 	for setting in settings:
	# 		if setting not in self.settings:
	# 			self.settings.append(setting)


default_section = Section('Settings')


# default_section: Section = Section
#
#
# def _setup_default_section():
# 	"""A separate function, so it can be called after directory has been set"""
# 	global default_section
# 	default_section = Section('Settings')



class Setting:
	"""Base setting class"""
	def __init__(self, datatype, name: str, default, section: Section = default_section):
		self.type = datatype
		self.name = name
		self.default = default
		self.section = section

		# if self.section == default_section and type(default_section) != section:
		# 	_setup_default_section()
		
		# self.section.add(self)
		self.section.settings.append(self)

		# Make sure that file/section/option exists
		if self.name not in self.section.file.keys():
			self.set(self.default)


	def get(self):
		return self.section.file.get(self.name, self.type)

	def set(self, new_value):
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
