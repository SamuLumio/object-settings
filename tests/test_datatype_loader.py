import settings

load = settings.backend.datatype_loader.get


def test_str():
	assert load("", str) == ""
	assert load("Test", str) == "Test"


def test_int():
	assert load(0, int) == 0
	assert load(5, int) == 5
	assert load("0", int) == 0
	assert load("5", int) == 5


def test_float():
	assert load(0.0, float) == 0
	assert load(1.5, float) == 1.5
	assert load("0.0", float) == 0
	assert load("1.5", float) == 1.5


def test_bool():
	assert load(True, bool) == True
	assert load(False, bool) == False
	assert load("True", bool) == True
	assert load("False", bool) == False
	assert load("yes", bool) == True
	assert load("no", bool) == False


def test_list():
	assert load([], list) == []
	assert load("[]", list) == []
	LIST = ["test", "1", "2"]
	assert load(LIST, list) == LIST
	assert load(str(LIST), list) == LIST

