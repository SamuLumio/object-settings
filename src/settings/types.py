import os, typing
from . import base, BaseSetting as _BaseSetting


# Yes, all of these overlayed methods have to exist for IDE features to work,
# one does not simply re- type hint an inherited variable





class Toggle(_BaseSetting):
	"""A boolean True/False"""

	def __init__(self, name, default: bool, section=base.default_section):
		super().__init__(bool, name, default, section)

	def get(self) -> bool:
		return bool(super().get())

	def set(self, new_value: bool):
		super().set(new_value)

	@property
	def value(self) -> bool:
		return self.get()

	@value.setter
	def value(self, new_value: bool):
		self.set(new_value)

	def toggle(self):
		self.set(not self.get())

	def __bool__(self):
		return self.value





class Choice(_BaseSetting):
	"""Choose an option (str) from a list"""

	def __init__(self, name, options: list[str], default: str, section=base.default_section):
		self.options = options
		super().__init__(str, name, default, section)

	def validate(self, value):
		return super().validate(value) and (value in self.options)

	def get(self) -> str:
		return str(super().get())

	def set(self, new_value: str):
		super().set(new_value)

	@property
	def value(self) -> str:
		return self.get()

	@value.setter
	def value(self, new_value: str):
		self.set(new_value)





class MappedChoice(Choice):
	"""Choose an option (str) from a list, but have a different internal value mapped to it. 
	Mappings are defined as a dictionary with internal values as keys and external values as values. 
	You can get the internal side of the current value with the `get_internal()` method 
	or the `internal_value` property. Otherwise behaves like normal Choice.
	\n
	For example, a logging level setting would have debug, info and error as user-facing values, 
	but 0, 1 and 2 as internal values: 
	`log_level = settings.MappedChoice("Level of logging", {0: "Debug", 1: "Info", 2: "Error"}, "Info")`
	"""

	def __init__(self, name, mappings: dict[typing.Any, str], default: str, section=base.default_section):
		self.mappings = mappings
		super().__init__(name, list(mappings.values()), default, section)

	def get_internal(self) -> typing.Any:
		"""Get the internal side of the current value"""
		value = self.get()
		for internal, external in self.mappings.items():
			if external == value:
				return internal
		raise KeyError("No mapping for current value. \
		 Did you change the options after setting creation without updating the mapping dictionary?")
	
	@property
	def internal_value(self) -> typing.Any:
		"""The internal side of the current value (cannot be set from here)"""
		return self.get_internal()





class Multichoice(_BaseSetting):
	"""Choose multiple options (str) from a list. 
	NOTE: getting the value returns a new list everytime, 
	so mutations to it won't apply to the stored value"""

	def __init__(self, name, options: list[str], default_choices: list[str], section=base.default_section):
		self.options = options
		super().__init__(list, name, default_choices, section)

	def validate(self, value):
		conditions = [
			super().validate(value),
			all((item in self.options) for item in value),
			all((type(item) == str) for item in value)
		]
		return all(conditions)

	def get(self) -> list[str]:
		return list(super().get())

	def set(self, new_value: list[str]):
		for value in new_value:
			if value not in self.options:
				raise ValueError(f"New value {new_value} not in options ({self.options})")
		super().set(new_value)

	@property
	def value(self) -> list[str]:
		return self.get()

	@value.setter
	def value(self, new_value: list[str]):
		self.set(new_value)

	def append(self, item: str):
		value = self.get()
		value.append(item)
		self.set(value)

	def remove(self, item: str):
		value = self.get()
		value.remove(item)
		self.set(value)





class MappedMultichoice(Multichoice):
	"""Choose multiple options (str) from a list, but have different internal values mapped to them. 
	Mappings are defined as a dictionary with internal values as keys and external values as values. 
	You can get the internal sides of the current choices with the `get_internal()` method 
	or the `internal_value` property. Otherwise behaves like normal Multichoice.
	\n
	For example, a file type selection could have common names as user-facing values, 
	but the file extensions as internal values: \n
	```
	filetypes = settings.MappedMultichoice(
		"Select file types", 
		{'.mp4': "Video", '.mp3': "Audio", '.vtt': "Subtitles"}, 
		default_choices=["Video", "Audio"]
	)
	``` """

	def __init__(self, name, mappings: dict[typing.Any, str], default_choices: list[str], 
	      section=base.default_section):
		self.mappings = mappings
		super().__init__(name, list(mappings.values()), default_choices, section)

	def get_internal(self) -> list[typing.Any]:
		"""Get the internal sides of the current choices"""
		value = self.get()
		value_internal = []
		for internal, external in self.mappings.items():
			if external in value:
				value_internal.append(internal)
		if len(value_internal) == len(value):
			return value_internal
		else:
			raise KeyError("No mappings for all current choices. \
			Did you change the options after setting creation without updating the mapping dictionary?")
	
	@property
	def internal_value(self) -> list[typing.Any]:
		"""The internal sides of the current choices (cannot be set from here)"""
		return self.get_internal()





class Array(_BaseSetting):
	"""An array of any arbitrary strings. 
	NOTE: getting the value returns an immutable tuple, but for convenience
	the values *can* be edited on the fly with the setting's append() and remove() methods."""

	def __init__(self, name, default: typing.Iterable[str] = [], section=base.default_section):
		super().__init__(list, name, default, section)

	def validate(self, value) -> bool:
		try:
			value = list(value)
		except:
			return False
		else:
			return super().validate(value) and all(isinstance(i, str) for i in value)

	def get(self) -> tuple:
		return tuple(super().get())

	def set(self, new_value: typing.Iterable):
		super().set(list(new_value))

	@property
	def value(self) -> tuple:
		return self.get()

	@value.setter
	def value(self, new_value: typing.Iterable):
		self.set(new_value)

	def append(self, item: str):
		temp_list = list(self.value)
		temp_list.append(item)
		self.set(temp_list)

	def remove(self, item: str):
		temp_list = list(self.value)
		temp_list.remove(item)
		self.set(temp_list)

	




class Text(_BaseSetting):
	"""Just normal text"""

	def __init__(self, name, default: str, section=base.default_section):
		super().__init__(str, name, default, section)

	def get(self) -> str:
		return str(super().get())

	def set(self, new_value: str):
		super().set(new_value)

	@property
	def value(self) -> str:
		return self.get()

	@value.setter
	def value(self, new_value: str):
		self.set(new_value)





class Path(_BaseSetting):
	"""A file path whose existence can be checked. 
	Automatically converted between Windows and Unix paths."""

	def __init__(self, name, default: str, has_to_exist: bool = False, section=base.default_section):
		self.has_to_exist = has_to_exist
		super().__init__(str, name, default, section)

	def validate(self, value):
		valid = super().validate(value)
		if self.has_to_exist:
			return valid and os.path.exists(value)
		else:
			return valid

	def get(self) -> str:
		return str(super().get())

	def set(self, new_value: str):
		if os.name == 'nt':
			new_value = new_value.replace('/', '\\')
		else:
			new_value = new_value.replace('\\', '/')
		super().set(new_value)

	@property
	def value(self) -> str:
		return self.get()

	@value.setter
	def value(self, new_value: str):
		self.set(new_value)





class Number(_BaseSetting):
	"""An integer that can be set or incremented and decremented"""

	def __init__(self, name, default: int, lower_limit: int = 0, upper_limit: int = 100,
	             section=base.default_section):
		self.lower_limit = lower_limit
		self.upper_limit = upper_limit
		super().__init__(int, name, default, section)

	def validate(self, value):
		if type(value) == int:  # The base method does check for this, but the size check could crash
			return super().validate(value) and (self.lower_limit <= value <= self.upper_limit)
		else:
			return False

	def get(self) -> int:
		return int(super().get())

	def set(self, new_value: int):
		super().set(new_value)

	@property
	def value(self) -> int:
		return self.get()

	@value.setter
	def value(self, new_value: int):
		self.set(new_value)

	def increment(self):
		self.set(self.get() + 1)

	def decrement(self):
		self.set(self.get() - 1)
