from dataclasses import dataclass as _dataclass
from settings.config import _instance


@_instance
@_dataclass
class strings:
	file: str = "File"
	dir: str = "Directory"
	set_from_env: str = "(set externally)"



