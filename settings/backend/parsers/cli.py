import sys, argparse

from . import _template



class CliOptionParser(_template.EnvironmentParser):

	@classmethod
	def generate_key_name(cls, setting_name: str):
		"""Generates a cli option name in the form --setting-name,
		with dashes, lowercase letters and no spaces or special characters"""
		name = setting_name.lower()
		for index, char in enumerate(name):
			if not char.islower():
				name = name.replace(char, '-')
		while '--' in name:
			name = name.replace('--', '-')
		name = name.strip('-')
		return '--' + name


	@classmethod
	def get(cls, key: str):
		index = sys.argv.index(key)
		next = index + 1
		if len(sys.argv) == next or sys.argv[next].startswith('--'):  # There's no value given
			return True  # Boolean flag
		else:
			return sys.argv[next]

	@classmethod
	def exists(cls, key: str):
		return key in sys.argv
