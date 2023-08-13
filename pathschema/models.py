from typing import Optional
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
import re
import fnmatch



class Necessity(Enum):
	"""Marks the necessity of a path"""
	OPTIONAL = 0
	REQUIRED = 1
	FORBIDDEN = 2



@dataclass
class PathNode:
	"""A schema path node"""

	name: str
	parent: Optional['PathNode'] = None
	necessity: Necessity = Necessity.OPTIONAL

	@property
	def is_regex(self) -> bool:
		return (
			self.name.startswith('"') and
			self.name.endswith('"')
		)

	@property
	def path(self) -> str:
		if self.parent is None:
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

		if self.is_regex:
			regex = self.name.removeprefix('"').removesuffix('"')
			match = re.fullmatch(regex, name)

			return match is not None

		return fnmatch.fnmatch(name, self.name)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name and
			self.necessity == other.necessity
		)

	def __str__(self) -> str:
		return f'node:{self.name}'

	def __repr__(self) -> str:
		return f'node:{self.name}'



@dataclass
class DirPathNode(PathNode):
	"""A schema directory path. Can hold multiple schema nodes"""

	childs: list['PathNode'] = field(default_factory=list)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name and
			self.necessity == other.necessity and
			len(self.childs) == len(other.childs) and
			self.childs == other.childs
		)

	def add_child(self, node: PathNode) -> 'DirPathNode':
		node.parent = self
		self.childs.append(node)
		return self

	def get_child_by_name(self, name) -> Optional['PathNode']:
		for node in self.childs:
			if node.name == name:
				return node

		return None

	def get_required_childs(self) -> list[PathNode]:
		return list(filter(lambda x: x.necessity == Necessity.REQUIRED, self.childs))

	def get_forbidden_childs(self) -> list[PathNode]:
		return list(filter(lambda x: x.necessity == Necessity.FORBIDDEN, self.childs))

	def get_matching_child(self, name) -> Optional['PathNode']:
		"""Get the first matching child, prioritizing forbidden"""

		sorted_childs = sorted(self.childs, key=lambda x: x.necessity == Necessity.FORBIDDEN, reverse=True)
		for node in sorted_childs:
			if node.validate_against(name):
				return node

		return None

	def __str__(self) -> str:
		return f'node:📁{self.name}/(childs:{len(self.childs)})'

	def __repr__(self) -> str:
		return f'node:📁{self.name}/(childs:{len(self.childs)})'



@dataclass
class FilePathNode(PathNode):
	"""A schema file path"""

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__) and
			self.name == other.name and
			self.necessity == other.necessity
		)

	def __str__(self) -> str:
		return f'node:📄{self.name}'

	def __repr__(self) -> str:
		return f'node:📄{self.name}'



@dataclass
class AnyPathNode(PathNode):
	"""A schema any path"""

	name: str = '...'
	necessity: Necessity = Necessity.OPTIONAL

	def validate_against(self, name: str) -> bool:
		return True

	def __eq__(self, other: object) -> bool:
		return isinstance(other, self.__class__)

	def __str__(self) -> str:
		return 'node:...'

	def __repr__(self) -> str:
		return 'node:...'



@dataclass
class ValidationResult:
	"""Holds all errors returned by a validation"""

	errors_by_path: dict[Path, list[str]] = field(default_factory=dict)

	def has_error(self):

		for errors in self.errors_by_path.values():
			if len(errors) > 0:
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
