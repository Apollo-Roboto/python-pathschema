from dataclasses import dataclass
from typing import Union, Optional
from pathlib import Path

sample_schema = {
	"root/": {
		"test.exe": None,
		"a_file.txt": None,
		"a_directory/": {
			
		}
	}
}

def validate(path: Union[str, Path]):
	if(isinstance(path, str)):
		path = Path(path)
	

@dataclass
class fssFile:
	parent: Optional['fssFile']
	childs: list['fssFile']
	
