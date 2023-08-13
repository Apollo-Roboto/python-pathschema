from typing import Union as _Union
from typing import Optional as _Optional
from pathlib import Path as _Path

from .validator import Validator
from .parser import Parser
from . import models
from . import exceptions



def validate(path: _Union[str, _Path], schema: str) -> models.ValidationResult:
	"""Validate a directory against a path schema"""

	validator = Validator()
	return validator.validate(path, schema)
