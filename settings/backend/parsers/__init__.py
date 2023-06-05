from . import _template
from ._template import StorageParserTemplate, EnvironmentParserTemplate

from . import cli, env, files


storage_parsers = [files.CfgParser, files.YamlParser, files.JsonParser]
environment_parsers = [cli.CliOptionParser, env.EnvVarParser]
