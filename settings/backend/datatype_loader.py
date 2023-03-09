import configparser

str_converter_functions = {
	str: str,
	int: int,
	float: float,
	bool: lambda string: configparser.ConfigParser.BOOLEAN_STATES[string],
	list: lambda string: string.removeprefix("['").removesuffix("']").split("', '")
}

def get(data, output_type: type[str | int | float | bool | list]):
	if isinstance(data, output_type):
		return data
	elif isinstance(data, str) and output_type in str_converter_functions:
		function = str_converter_functions[output_type]
		return function(data)
	else:
		raise UnsupportedDataError(type(data))


class UnsupportedDataError(BaseException):
	def __init__(self, data_type: type):
		super().__init__(f"loading for source data type {data_type} is unsupported")
