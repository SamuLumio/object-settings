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


def test_float_special_methods():
	float = settings.Float("FloatSpecialTest", 0, 2, 0, 10000)
	float.set(5)
	float.increment()
	assert float.get() == 6.0
	float.decrement()
	assert float.get() == 5.0
	# Test imprecision correcting
	float.set(0.45)
	for i in range(1000):
		float.increment()
	assert float.get() == 1000.45



