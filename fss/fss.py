from dataclasses import dataclass, field
from typing import Union, Optional
from pathlib import Path
import re
import fnmatch



@dataclass
class fssNode:
	name: str
	forbidden: bool = False
	required: bool = False
	parent: Optional['fssNode'] = None

	@property
	def is_regex(self) -> bool:
		return (
			self.name.startswith('"') and
			self.name.endswith('"')
		)
	
	@property
	def path(self) -> str:
		if self.parent == None:
			return self.name
		return self.parent.path + '/' + self.name

	def validate_against(self, name: str) -> bool:
		"""
		Validate a given name against this node's name
		A validation is successful if
			The given name is a direct match to the node
			The given matches the regex
			The node is a match all `*`
		"""
		
		if(self.is_regex):
			regex = self.name.removeprefix('"').removesuffix('"')
			match = re.fullmatch(regex, name)
			
			return match != None
		
		return fnmatch.fnmatch(name, self.name)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name
		)

	def __str__(self) -> str:
		return f'node:{self.name}'
	
	def __repr__(self) -> str:
		return f'node:{self.name}'

@dataclass
class fssDirNode(fssNode):
	childs: list['fssNode'] = field(default_factory=list)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name and
			len(self.childs) == len(other.childs) and
			self.childs == other.childs
		)

	def add_child(self, node: fssNode) -> 'fssDirNode':
		node.parent = self
		self.childs.append(node)
		return self

	def get_child_by_name(self, name) -> Optional['fssNode']:
		for node in self.childs:
			if node.name == name:
				return node

		return None

	def get_required_childs(self) -> list[fssNode]:
		return list(filter(lambda x: x.required, self.childs))

	def get_matching_child(self, name) -> Optional['fssNode']:
		"""Get the first matching child, prioritizing forbidden"""

		sorted_childs = sorted(self.childs, key=lambda x: x.forbidden, reverse=True)
		for node in sorted_childs:
			if node.validate_against(name):
				return node

		return None

	def required_satisfied(self, name) -> bool:

		# for each child that are required
		for child in self.childs:
			if(not child.required):
				continue

			match = child.validate_against(name)

		return True

	def __str__(self) -> str:
		return f'node:📁{self.name}/(childs:{len(self.childs)})'

	def __repr__(self) -> str:
		return f'node:📁{self.name}/(childs:{len(self.childs)})'

@dataclass
class fssFileNode(fssNode):

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name
		)

	def __str__(self) -> str:
		return f'node:📄{self.name}'

	def __repr__(self) -> str:
		return f'node:📄{self.name}'

@dataclass
class fssAnyNode(fssNode):
	name: str = '...'

	def validate_against(self, name: str) -> bool:
		return True

	def __eq__(self, other: object) -> bool:
		return isinstance(other, self.__class__)

	def __str__(self) -> str:
		return f'node:...'

	def __repr__(self) -> str:
		return f'node:...'

@dataclass
class ValidationResult:
	errors_by_path: dict[Path, list[str]] = field(default_factory=dict) 

	def has_error(self):

		for errors in self.errors_by_path.values():
			if(len(errors) > 0):
				return True

		return False

	def get_errors(self, path: Path) -> Optional[list[str]]:
		return self.errors_by_path.get(path, None)

	def add_error(self, path: Path, error: str):

		# init value if doesn't exists
		self.errors_by_path[path] = self.errors_by_path.get(path, [])

		# add error to the path
		self.errors_by_path[path].append(error)

	def add_path(self, path):
		self.errors_by_path[path] = self.errors_by_path.get(path, [])

	def update(self, other: 'ValidationResult'):
		self.errors_by_path.update(other.errors_by_path)