import os.path

import settings

dummy_options = ["1", "2", "3"]


def _base_validate(setting: settings.base.Setting, valid_values: list, invalid_values: list):
	for valid_value in valid_values:
		assert setting.validate(valid_value)
	for invalid_value in invalid_values:
		assert not setting.validate(invalid_value)



def test_toggle():
	_base_validate(
		setting=settings.Toggle("TestToggle", bool()),
		valid_values=[True, False],
		invalid_values=["baba", [False, True], 69]
	)


def test_choice():
	_base_validate(
		setting=settings.Choice("TestChoice", dummy_options, "1"),
		valid_values=dummy_options,
		invalid_values=[1, 2, 3, "0", "4", "yo mama"]
	)


def test_multichoice():
	_base_validate(
		setting=settings.Multichoice("TestMultichoice", dummy_options, ["1", "2"]),
		valid_values=[["1", "2"], ["1", "2", "3"], ["2"]],
		invalid_values=["1", "2", "3", [1, 2], ["sgrgs", "sgfd", "jhig"], ["ben", "2"]]
	)


def test_array():
	_base_validate(
		setting=settings.Array("TestArray"),
		valid_values=[["abc", "2"], ["h"], []],
		invalid_values=[True, 420, [1, 2, 3]]
	)


def test_text():
	_base_validate(
		setting=settings.Text("TestText", "default"),
		valid_values=["Any", "string", ""],
		invalid_values=[3, False, ["a", "b"]]
	)


def test_path():
	_base_validate(
		setting=settings.Path("TestPath", __file__, has_to_exist=True),
		valid_values=[__file__],
		invalid_values=[os.path.join(__file__, "dir that can't exist")]
	)


def test_number():
	_base_validate(
		setting=settings.Number("TestNumber", 3, -10, 10),
		valid_values=[-10, -5, 0, 5, 10],
		invalid_values=[-11, 11, 69, "some string", [2]]
	)
