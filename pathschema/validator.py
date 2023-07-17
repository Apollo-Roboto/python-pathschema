from typing import Union
from pathlib import Path
import os

from pathschema.parser import Parser
from pathschema.models import DirPathNode, FilePathNode, PathNode, ValidationResult, Necessity



class Validator():
	"""Validate a path against a path schema"""

	def __init__(self):
		pass

	def validate(self, path: Union[str, Path], schema: str) -> ValidationResult:
		if isinstance(path, str):
			path = Path(path)

		if not path.exists():
			raise ValueError('The path does not exists')

		if not path.is_dir():
			raise ValueError('The path to validate must be a directory')

		schema_node_tree = Parser().schema_to_node_tree(schema)

		# print_node_tree(schema_node_tree)

		results = self._validation_helper(path.absolute(), schema_node_tree)

		return results

	def _validation_helper(self, directory_to_validate: Path, node: PathNode) -> ValidationResult:

		current_node = node
		current_path = directory_to_validate

		results = ValidationResult()

		results.add_path(current_path)

		# mismatch: node is directory, path is file
		if(isinstance(current_node, DirPathNode) and not current_path.is_dir()):
			results.add_error(current_path, 'Expected a directory')
			return results

		# mismatch: node is file, path is dir
		if(isinstance(current_node, FilePathNode) and not current_path.is_file()):
			results.add_error(current_path, 'Expected a file')
			return results

		if(isinstance(current_node, DirPathNode) and current_path.is_dir()):

			required_childs = current_node.get_required_childs()

			# for each child of the current path
			for name in os.listdir(current_path):
				path = current_path / name

				results.add_path(path)

				# check if it matches a required child and remove
				i = 0
				while i < len(required_childs):
					required_child = required_childs[i]

					# if this child is satisfied
					if required_child.validate_against(name):
						required_childs.pop(i)
						continue

					i += 1

				matching_node = current_node.get_matching_child(name)

				# if there is no match
				if matching_node is None:
					results.add_error(path, 'Path not allowed')
					continue

				# if folder is forbidden
				if(isinstance(matching_node, DirPathNode) and matching_node.necessity == Necessity.FORBIDDEN):
					results.add_error(path, 'Folder forbidden')
					continue

				# if file is forbidden
				if(isinstance(matching_node, FilePathNode) and matching_node.necessity == Necessity.FORBIDDEN):
					results.add_error(path, 'File forbidden')
					continue

				sub_results = self._validation_helper(path, matching_node)

				results.update(sub_results)

			# if the list of required childs is not empty, there are missing requirements
			for child in required_childs:
				if isinstance(child, DirPathNode):
					results.add_error(current_path, f'Missing required folder {child.name}')
				if isinstance(child, FilePathNode):
					results.add_error(current_path, f'Missing required file {child.name}')

		return results
