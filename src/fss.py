from dataclasses import dataclass
from typing import Union, Optional
from pathlib import Path

sample_schema = """
root/
	text.exe
	a_file.txt
	a_directory/
"""

def validate(path: Union[str, Path], schema: str):
	if(isinstance(path, str)):
		path = Path(path)

@dataclass
class fssFile:
	name: str
	parent: Optional['fssFile']
	childs: list['fssFile']

	@property
	def is_dir(self):
		return self.name.endswith('/')
