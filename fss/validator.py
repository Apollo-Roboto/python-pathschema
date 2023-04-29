from typing import Union
from pathlib import Path
import os
from typing import Optional
from dataclasses import dataclass

from fss.parser import Parser
from fss.utils import print_node_tree
from fss.fss import fssDirNode, fssFileNode, fssNode, ValidationResult



class Validator():

	def __init__(self):
		pass

	def validate(self, path: Union[str, Path], schema: str) -> ValidationResult:
		if(isinstance(path, str)):
			path = Path(path)

		if(not path.exists()):
			raise ValueError('The path does not exists')
		
		if(not path.is_dir()):
			raise ValueError('The path to validate must be a directory')

		schema_node_tree = Parser().schema_to_node_tree(schema)

		print_node_tree(schema_node_tree)

		results = self._validation_helper(path.absolute(), schema_node_tree)

		return results
		
	def _validation_helper(self, directory_to_validate: Path, node: fssNode) -> ValidationResult:

		current_node = node
		current_path = directory_to_validate

		results = ValidationResult()

		results.add_path(current_path)

		# mismatch: node is directory, path is file
		if(isinstance(current_node, fssDirNode) and not current_path.is_dir()):
			results.add_error(current_path, 'Expected a directory')
			return results

		# mismatch: node is file, path is dir
		if(isinstance(current_node, fssFileNode) and not current_path.is_file()):
			results.add_error(current_path, 'Expected a file')
			return results

		if(isinstance(current_node, fssDirNode) and current_path.is_dir()):
			for name in os.listdir(current_path):
				path = current_path / name

				results.add_path(path)

				matching_node = current_node.get_matching_child(name)

				if(matching_node == None):
					results.add_error(path, 'No match found')
					continue

				if(isinstance(matching_node, fssDirNode) and matching_node.forbidden):
					results.add_error(path, 'Folder Forbidden')
					continue

				if(isinstance(matching_node, fssFileNode) and matching_node.forbidden):
					results.add_error(path, 'File Forbidden')
					continue

				sub_results = self._validation_helper(path, matching_node)

				results.update(sub_results)

		return results
