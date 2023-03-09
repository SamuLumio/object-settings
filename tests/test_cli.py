import sys

import settings

parser = settings.backend.parsers.cli.CliOptionParser()

key = '--cli-test'
value = "working"

setting = settings.Text("Cli test", "if you see this it's not working")


def test_cli_key_generation():
	assert parser.generate_key_name(setting.name) == key
	assert parser.generate_key_name(" * Extra-signs test!!! * ") == '--extra-signs-test'


def test_option_parse():
	sys.argv.extend([key, value])
	assert parser.get(key) == value
	sys.argv.append('--flag')
	assert parser.get('--flag') is True
	sys.argv.append('--another-option')
	assert parser.get('--flag') is True


def test_data_conversion():
	s = settings.Number('cli number', 2)
	sys.argv.extend(['--cli-number', "5"])
	assert s.get() == 5


def test_cli_inpractice():
	sys.argv.remove(key)
	setting.reset()
	assert not setting.set_externally
	sys.argv.extend([key, value])
	assert setting.set_externally
	assert setting.get() == value
