from dataclasses import dataclass, field
from typing import Union, Optional
from pathlib import Path
import re
import fnmatch



@dataclass
class fssNode:
	name: str
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
	
	def get_matching_child(self, name) -> Optional['fssNode']:
		for node in self.childs:
			if node.validate_against(name):
				return node

		return None

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
