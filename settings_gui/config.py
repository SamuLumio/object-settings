from dataclasses import dataclass as _dataclass


def _config(cls):
	# Editable by calling
	cls.__call__ = cls.__init__
	# Return instance
	return cls()



@_config
@_dataclass
class strings:
	file: str = "File"
	dir: str = "Directory"



