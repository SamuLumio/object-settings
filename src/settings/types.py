import os
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





class Multichoice(_BaseSetting):
	"""Choose multiple options (str) from a list"""
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
	"""A file path. Automatically converted between Windows and Unix paths."""
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
	"""A number (int) that can be incremented and decremented"""
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
