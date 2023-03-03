from dataclasses import dataclass as _dataclass
from settings.config import _config


@_config
@_dataclass
class strings:
	file: str = "File"
	dir: str = "Directory"



