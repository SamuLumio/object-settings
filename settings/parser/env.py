import os, typing

from .. import config
from . import _datatype_loader


def generate_key_name(setting_name: str):
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

	return f"{convert(config.app_name)}_{convert(setting_name)}"


def get(setting_name: str, type: typing.Type[str | int | float | bool | list]):
	key = generate_key_name(setting_name)
	string = os.environ[key]
	return _datatype_loader.functions[type](string)

def exists(setting_name: str):
	key = generate_key_name(setting_name)
	return key in os.environ.keys()

