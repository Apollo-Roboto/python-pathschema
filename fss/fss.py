from dataclasses import dataclass, field
from typing import Union, Optional
from pathlib import Path
import re

illegalCharacters = ['\\', '/', '?', '*', ':', '|', '"', '<', '>']
# dot '.' is not allowed at the end of a directory

@dataclass
class fssNode:
	name: str
	parent: Optional['fssNode'] = None

	@property
	def is_regex(self) -> bool:
		return \
			self.name.startswith('"') and \
			self.name.endswith('"')

	@property
	def is_match_all(self) -> bool:
		return self.name == '*'

	def validate_against(self, name: str) -> bool:
		"""Validate a given name against this node's name"""

		if(self.is_match_all):
			return True
		
		if(self.is_regex):
			regex = self.name.removeprefix('"').removesuffix('"')
			match = re.fullmatch(regex, name)
			
			return match != None
		
		return self.name == name

	def __eq__(self, __value: object) -> bool:
		return \
			isinstance(__value, fssNode) and \
			self.name == __value.name and \
			self.parent == __value.parent

@dataclass
class fssDirNode(fssNode):
	childs: list['fssNode'] = field(default_factory=list)

	def __eq__(self, __value: object) -> bool:
		return \
			isinstance(__value, fssDirNode) and \
			self.name == __value.name and \
			self.parent == __value.parent

	def add_child(self, node: fssNode) -> 'fssDirNode':
		node.parent = self
		self.childs.append(node)
		return self

@dataclass
class fssFileNode(fssNode):
	def __eq__(self, __value: object) -> bool:
		return \
			isinstance(__value, fssFileNode) and \
			self.name == __value.name and \
			self.parent == __value.parent
