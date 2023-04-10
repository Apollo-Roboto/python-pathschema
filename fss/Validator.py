from typing import Union
from pathlib import Path
import os

from fss.Parser import Parser
from fss.utils import print_node_tree
from fss.fss import fssDirNode
from fss.exceptions import ValidationError

def validate(path: Union[str, Path], schema: str):
	if(isinstance(path, str)):
		path = Path(path)

	if(not path.exists()):
		raise ValueError('The path does not exists')
	
	if(not path.is_dir()):
		raise ValueError('The path to validate must be a directory')

	node_tree = Parser().schema_to_node_tree(schema)

	# for (dir_path, dir_names, file_names) in os.walk(path):
	# 	print(dir_path)
	# 	print(dir_names)
	# 	print(file_names)
	# 	pass

	print_node_tree(node_tree, sort=True)

	# currently only able to validate one level

	dir_valid = _validate_directory(path, node_tree)

	# if one of the values is false, validation failed
	if(not all(dir_valid.values())):
		raise ValidationError('The directory was not valid')

def _validate_directory(directory: Path, node: fssDirNode) -> dict[str, bool]:

	print(f'going to validate directory {directory} with node {node.name}')

	dir_valid: dict[str, bool] = {}

	elements = os.listdir(directory)

	for element in elements:

		dir_valid.update({element: False})
		for child in node.childs:
			
			if(child.validate_against(element)):
				dir_valid.update({element: True})
				break

	print(dir_valid)

	return dir_valid
