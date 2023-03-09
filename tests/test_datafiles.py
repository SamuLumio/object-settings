import settings




json = """
{
	"json_string": "json_string_value",
	"json_list": [
		"item 1",
		"item 2"
	]
}
"""


def test_json():
	# section = settings.Section("Json test")
	parser = settings.backend.parsers.files.JsonParser("Json test")
	with open(parser.path, 'w') as file:
		file.write(json)
	assert parser.get("json_string") == "json_string_value"
	assert parser.get("json_list") == ["item 1", "item 2"]






yaml = """
yaml_string: yaml_string_value
yaml_list:
  - item 1
  - item 2
"""

def test_yaml():
	# section = settings.Section("Json test")
	parser = settings.backend.parsers.files.YamlParser("Yaml test")
	with open(parser.path, 'w') as file:
		file.write(yaml)
	assert parser.get("yaml_string") == "yaml_string_value"
	assert parser.get("yaml_list") == ["item 1", "item 2"]

