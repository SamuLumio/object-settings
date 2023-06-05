import appdirs, os, configparser, json, yaml

from . import StorageParserTemplate



class _FileParser(StorageParserTemplate):
	ext: str

	def __init__(self, header="Settings"):
		super().__init__(header)
		self.values: dict = {}

	@property
	def path(self):
		from .. import config
		if isinstance(config.custom_dir, str):
			dir = config.custom_dir
		else:
			dir = appdirs.user_config_dir(config.app_name, False)
		return os.path.join(dir, self.header + self.ext)

	def _read(self):
		"""Load values from file"""
		# Subclass

	def _write(self):
		"""Dump all current values to the file."""
		os.makedirs(os.path.dirname(self.path), exist_ok=True)
		# Subclass

	def get(self, option: str):
		self._read()
		return self.values[option]

	def set(self, option: str, value):
		self.values[option] = value
		self._write()

	def exists(self, option: str):
		try:
			self._read()
			return option in self.values
		except:
			return False

	@property
	def active(self):
		return os.path.exists(self.path)






class CfgParser(_FileParser):
	ext = '.cfg'

	def __init__(self, header="Settings"):
		super().__init__(header)
		# Initialize lower-level config parser
		self._parser = configparser.ConfigParser()
		self._parser.optionxform = str  # For preserve case    # type: ignore

	def _read(self):
		self._parser.read(self.path)
		# Make sure that header section exists
		if self.header not in self._parser.sections():
			self._parser.add_section(self.header)
		self.values = dict(self._parser[self.header])

	def _write(self):
		super()._write()
		self._parser[self.header] = {str(key): str(value) for key, value in self.values.items()}
		with open(self.path, 'w') as f:
			self._parser.write(f)



class YamlParser(_FileParser):
	ext = '.yaml'

	def _read(self):
		with open(self.path) as file:
			values = yaml.load(file, yaml.Loader)
		self.values = values

	def _write(self):
		super()._write()
		with open(self.path, 'w') as f:
			yaml.dump(self.values, f)



class JsonParser(_FileParser):
	ext = '.json'

	def _read(self):
		with open(self.path) as file:
			values = json.load(file)
		self.values = values

	def _write(self):
		super()._write()
		with open(self.path, 'w') as f:
			json.dump(self.values, f)
