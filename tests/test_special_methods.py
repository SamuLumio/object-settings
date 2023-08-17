import settings


def test_toggle_special_methods():
	toggle = settings.Toggle("ToggleSpecialTest", True)
	toggle.set(True)
	toggle.toggle()
	assert toggle.get() == False
	toggle.toggle()
	assert toggle.get() == True


def test_array_special_methods():
	array = settings.Array("ArraySpecialTest")
	array.set(['a', 'b', 'c'])
	array.append('d')
	assert array.get() == ('a', 'b', 'c', 'd')
	array.remove('b')
	assert array.get() == ('a', 'c', 'd')


def test_number_special_methods():
	number = settings.Number("NumberSpecialTest", 0)
	number.set(5)
	number.increment()
	assert number.get() == 6
	number.decrement()
	assert number.get() == 5


