import configparser

functions = {
	str: str,
	int: int,
	float: float,
	bool: lambda string: configparser.ConfigParser.BOOLEAN_STATES[string],
	list: lambda string: string.strip("['").strip("']").split("', '")
}
