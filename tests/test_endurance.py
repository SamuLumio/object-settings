import configparser
import os, shutil

import settings


setting = settings.Number("Dummy", 5)
path = setting.section.get_path()


def _check():
	assert setting.get() == 5



def test_file_deletion():
	os.remove(path)
	_check()


def test_dir_deletion():
	shutil.rmtree(os.path.dirname(path))
	_check()


def test_file_replacement():
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as file:
		file.write("replaced content")
	_check()


def test_invalid_edit():
	parser = configparser.ConfigParser()
	parser.add_section(setting.section.name)
	parser.set(setting.section.name, setting.name, "some string")
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, 'w') as file:
		parser.write(file)
	_check()
