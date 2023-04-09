from dataclasses import dataclass, field
from typing import Union, Optional
from pathlib import Path

illegalCharacters = ['\\', '?', '%', '*', ':', '|', '"', '<', '>', '']
# dot '.' is not allowed at the end of a directory

def validate(path: Union[str, Path], schema: str):
	if(isinstance(path, str)):
		path = Path(path)


@dataclass
class fssNode:
	name: str
	parent: Optional['fssNode'] = None
	childs: list['fssNode'] = field(default_factory=list)

	@property
	def is_dir(self):
		return self.name.endswith('/')
	
	@property
	def is_file(self):
		return not self.name.endswith('/')
	
	def validate_name(self):
		for i, character in enumerate(self.name):
			if character in illegalCharacters:
				return False
		
		return True
