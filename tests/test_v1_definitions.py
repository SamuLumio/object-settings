"""Test that settings defined with the first version of the library still work"""

import settings



def test_toggle():
	setting = settings.Toggle("v1 test toggle", True)
	assert setting.name == "v1 test toggle"
	assert setting.default is True


def test_choice():
	setting = settings.Choice("v1 test choice", ["1", "2", "3"], "2")
	assert setting.name == "v1 test choice"
	assert setting.options == ["1", "2", "3"]
	assert setting.default == "2"


def test_multichoice():
	setting = settings.Multichoice("v1 test multichoice", ["1", "2", "3"], ["1", "3"])
	assert setting.name == "v1 test multichoice"
	assert setting.options == ["1", "2", "3"]
	assert setting.default == ["1", "3"]


def test_text():
	setting = settings.Text("v1 test text", "Test")
	assert setting.name == "v1 test text"
	assert setting.default == "Test"


def test_path():
	setting = settings.Path("v1 test path", "/test")
	assert setting.name == "v1 test path"
	assert setting.default == "/test"


def test_number():
	setting = settings.Number("v1 test number", 3)
	assert setting.name == "v1 test number"
	assert setting.default == 3
