import os

from . import _template



class EnvVarParser(_template.EnvironmentParser):

	@classmethod
	def generate_key_name(cls, setting_name: str):
		"""Generates an envvar key in the form APPNAME_SETTING_NAME,
		with underscores, capital letters and no spaces or special characters"""

		def convert(string: str):
			string = string.upper()
			for index, char in enumerate(string):
				if not char.isupper():
					string = string.replace(char, '_')
			while '__' in string:
				string = string.replace('__', '_')
			string = string.strip('_')
			return string

		from .. import config
		return f"{convert(config.app_name)}_{convert(setting_name)}"


	@classmethod
	def get(cls, key: str):
		string = os.environ[key]
		return string

	@classmethod
	def exists(cls, key: str):
		return key in os.environ.keys()
