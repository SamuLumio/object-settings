import typing


class EnvironmentParserTemplate:
	"""Controller/parser for a read-only config source"""

	@classmethod
	def generate_key_name(cls, setting_name: str) -> str:
		"""Generate a key name that a setting can be found with"""
		return str(setting_name)

	@classmethod
	def get(cls, option: str) -> typing.Any:
		"""Reload and get value"""

	@classmethod
	def exists(cls, option: str) -> bool:
		"""Check if option is defined"""
		return False




class StorageParserTemplate:
	"""Controller/parser for a config file"""

	def __init__(self, header="Settings"):
		self.header = header

	def get(self, option: str) -> typing.Any:
		"""Reload and get value"""

	def set(self, option: str, value):
		"""Set a value and write to storage"""

	def exists(self, option: str) -> bool:
		"""Check if option is defined"""
		return False

	@property
	def active(self) -> bool:
		"""Check if a stored configuration exists"""
		return False
