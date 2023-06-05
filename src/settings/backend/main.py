from . import config, datatype_loader



class Storage:
	def __init__(self, header: str):
		self.header = header
		self.parser = self._get_parser()

		self.set = self.parser.set
		self.exists = self.parser.exists
		self.active = self.parser.active


	def get(self, option: str, type: type[str | int | float | bool | list]):
		data = self.parser.get(option)
		value = datatype_loader.get(data, type)
		return value


	def _get_parser(self):
		if not config.storage_parsers:
			raise self.NoParsersError

		# Check if any stored values already exist
		for parser_type in config.storage_parsers:
			parser = parser_type(self.header)
			if parser.active:
				return parser

		# If not, create a new parser of the first preferred type
		return config.storage_parsers[0](self.header)


	class NoParsersError(BaseException):
		def __init__(self):
			super().__init__("storage parser list is empty")




class Environment:
	def __init__(self):
		self.parsers = config.environment_parsers


	def get(self, option: str, type: type[str | int | float | bool | list]):
		for parser in self.parsers:
			try:
				key = parser.generate_key_name(option)
				data = parser.get(key)
				return datatype_loader.get(data, type)
			except:
				pass
		raise KeyError(f"option not found in environment (parsers: {', '.join(str(p) for p in self.parsers)}")

	def exists(self, option: str):
		for parser in self.parsers:
			key = parser.generate_key_name(option)
			if parser.exists(key):
				return True
		return False
