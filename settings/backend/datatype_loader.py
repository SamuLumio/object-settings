import configparser

str_converter_functions = {
	str: str,
	int: int,
	float: float,
	bool: lambda string: configparser.ConfigParser.BOOLEAN_STATES[string.lower()],
	list: lambda string: string.removeprefix("['").removesuffix("']").split("', '")
}

def get(data, output_type: type[str | int | float | bool | list]):
	if isinstance(data, output_type):
		return data
	elif isinstance(data, float) and output_type == int:
		return int(data)
	elif isinstance(data, str) and output_type in str_converter_functions:
		function = str_converter_functions[output_type]
		return function(data)
	else:
		raise UnsupportedDataError(type(data), output_type)


class UnsupportedDataError(BaseException):
	def __init__(self, data_type: type, wanted_type: type):
		super().__init__(f"loading {data_type} source data as {wanted_type} is unsupported")
