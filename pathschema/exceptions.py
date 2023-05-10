from typing import Optional
from pathlib import Path

class SchemaError(Exception):
	"""An error in the path schema definition"""

	def __init__(self, msg: str, line_num: int, schema_path: Optional[Path]=None, *args: object) -> None:
		if schema_path:
			message = f'{msg} ({schema_path}, line {line_num})'
		else:
			message = f'{msg} (at line {line_num})'

		super().__init__(message, *args)
