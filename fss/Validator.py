from typing import Union
from pathlib import Path
import os

from fss.Parser import Parser
from fss.utils import print_node_tree
from fss.fss import fssDirNode
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

		print_node_tree(schema_node_tree, sort=True)

		base_path = path

		valid = self._recursive_validation(path, schema_node_tree)
		if(not valid):
			raise ValidationError('The directory was not valid')

	def _recursive_validation(self, directory: Path, node: fssDirNode) -> bool:

		dir_valid = True

		for sub_dir_name in os.listdir(directory):
			print(f'{sub_dir_name}')

			matching_name = False
			matching_node = None

			# one match in one of the child and this name is valid
			for child in node.childs:
				if(child.validate_against(sub_dir_name)):
					print(f'  {sub_dir_name} matches {child}')

					matching_name = True
					matching_node = child
					break

			if(matching_name):

				dir_valid = True

				# Validate the files in this sub directory
				if matching_node != None and isinstance(matching_node, fssDirNode):
					new_directory = Path(directory, sub_dir_name)

					# if one of the childs is invalid, this directory is invalid
					dir_valid = self._recursive_validation(new_directory, matching_node)
			
			else:
				dir_valid = False

		print(f'directory {directory} is {dir_valid}')
		return dir_valid

	def _validate_directory(self, directory: Path, node: fssDirNode) -> dict[str, bool]:

		dir_valid: dict[str, bool] = {}

		elements = os.listdir(directory)

		for element in elements:

			dir_valid.update({element: False})
			for child in node.childs:
				
				if(child.validate_against(element)):
					dir_valid.update({element: True})
					break

		return dir_valid
