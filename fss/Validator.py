from typing import Union
from pathlib import Path
import os
from typing import Optional

from fss.parser import Parser
from fss.utils import print_node_tree
from fss.fss import fssDirNode, fssFileNode, fssNode
from fss.exceptions import ValidationError



class Validator():

	def __init__(self):
		pass

	def validate(self, path: Union[str, Path], schema: str):
		if(isinstance(path, str)):
			path = Path(path)

		if(not path.exists()):
			raise ValueError('The path does not exists')
		
		if(not path.is_dir()):
			raise ValueError('The path to validate must be a directory')

		schema_node_tree = Parser().schema_to_node_tree(schema)

		print_node_tree(schema_node_tree)

		valid = self._validation_helper(path, schema_node_tree)
		if(not valid):
			raise ValidationError('The directory was not valid')
		
	def _validation_helper(self, directory_to_validate: Path, node: Optional['fssNode']) -> bool:

		current_node = node
		current_path = directory_to_validate

		if(isinstance(current_node, fssDirNode)):
			
			# mismatch: node is directory, path is file
			if(current_path.is_file()):
				return False

			for name in os.listdir(current_path):
				path = current_path / name

				matching_node = current_node.get_matching_child(name)

				valid = self._validation_helper(path, matching_node)
				if(not valid):
					return False
			
			return True
		
		elif(isinstance(current_node, fssFileNode)):

			# mismatch: node is file, path is dir
			if(current_path.is_dir()):
				return False
		
		if(current_node == None):
			return False
		
		return current_node.validate_against(current_path.name)
