from typing import Union as _Union
from typing import Optional as _Optional
from pathlib import Path as _Path

from .validator import Validator
from .parser import Parser
from . import models
from . import exceptions



def validate(path: _Union[str, _Path], schema: str, schema_path: _Optional[_Path]=None) -> models.ValidationResult:
	validator = Validator()
	return validator.validate(path, schema, schema_path)
