from . import _template, cli, env, files

from ._template import StorageParser, EnvironmentParser



storage_parsers = [files.CfgParser, files.YamlParser, files.JsonParser]
environment_parsers = [cli.CliOptionParser, env.EnvVarParser]
