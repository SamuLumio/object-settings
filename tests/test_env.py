import os, pytest

import settings
from settings.parser import env as parser


key = 'TESTAPP_ENVTEST'
value = "this value is from the enviroment variable"

setting = settings.Text("Envtest", "not the value from the enviroment variable")


def test_env_key_generation():
	assert parser.generate_key_name(setting.name) == key
	assert parser.generate_key_name(" * Extra-signs test!!! * ") == 'TESTAPP_EXTRA_SIGNS_TEST'


def test_env_read():
	os.environ[key] = value
	assert parser.get('ENVTEST', str) == value


def test_data_conversion():
	s = settings.Number('bruh', 2)
	os.environ['TESTAPP_BRUH'] = '5'
	assert s.get() == 5


def test_write_block():
	os.environ[key] = value
	pytest.raises(PermissionError, setting.set, "anything")


def test_env_inpractice():
	os.environ.pop(key)
	setting.reset()
	assert not setting.set_from_env
	os.environ[key] = value
	assert setting.set_from_env
	assert setting.get() == value
