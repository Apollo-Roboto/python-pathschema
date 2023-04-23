from typing import Union
from pathlib import Path
import os
from typing import Optional
from dataclasses import dataclass

from fss.parser import Parser
from fss.utils import print_node_tree
from fss.fss import fssDirNode, fssFileNode, fssNode
from fss.exceptions import ValidationError



class Validator():

	def __init__(self):
		pass

	def validate(self, path: Union[str, Path], schema: str) -> dict[Path, list[str]]:
		if(isinstance(path, str)):
			path = Path(path)

		if(not path.exists()):
			raise ValueError('The path does not exists')
		
		if(not path.is_dir()):
			raise ValueError('The path to validate must be a directory')

		schema_node_tree = Parser().schema_to_node_tree(schema)

		errors = self._validation_helper(path.absolute(), schema_node_tree)

		return errors
		
	def _validation_helper(self, directory_to_validate: Path, node: fssNode) -> dict[Path, list[str]]:

		current_node = node
		current_path = directory_to_validate

		errors_by_path: dict[Path, list[str]] = {}

		errors_by_path[current_path] = errors_by_path.get(current_path, [])

		# mismatch: node is directory, path is file
		if(isinstance(current_node, fssDirNode) and not current_path.is_dir()):
			errors_by_path[current_path].append('Expected a directory')
			return errors_by_path

		# mismatch: node is file, path is dir
		if(isinstance(current_node, fssFileNode) and not current_path.is_file()):
			errors_by_path[current_path].append('Expected a file')
			return errors_by_path

		if(isinstance(current_node, fssDirNode) and current_path.is_dir()):
			
			for name in os.listdir(current_path):
				path = current_path / name

				errors_by_path[path] = errors_by_path.get(path, [])

				matching_node = current_node.get_matching_child(name)

				if(matching_node == None):
					errors_by_path[path].append(f'Not allowed in {current_node.path}')
					continue
				
				sub_errors = self._validation_helper(path, matching_node)

				errors_by_path.update(sub_errors)

		return errors_by_path
