import os, pytest

import settings


parser = settings.backend.parsers.env.EnvVarParser()

key = 'TESTAPP_ENVTEST'
value = "this value is from the enviroment variable"

setting = settings.Text("Envtest", "not the value from the enviroment variable")


def test_env_key_generation():
	assert parser.generate_key_name(setting.name) == key
	assert parser.generate_key_name(" * Extra-signs test!!! * ") == 'TESTAPP_EXTRA_SIGNS_TEST'


def test_env_read():
	os.environ[key] = value
	assert parser.get(key) == value


def test_data_conversion():
	s = settings.Number('env number', 2)
	os.environ['TESTAPP_ENV_NUMBER'] = '5'
	assert s.get() == 5




def test_env_inpractice():
	os.environ.pop(key)
	setting.reset()
	assert not setting.set_externally
	os.environ[key] = value
	assert setting.set_externally
	assert setting.get() == value
