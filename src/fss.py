from dataclasses import dataclass, field
from typing import Union, Optional
from pathlib import Path

illegalCharacters = ['\\', '/', '?', '*', ':', '|', '"', '<', '>']
# dot '.' is not allowed at the end of a directory

def validate(path: Union[str, Path], schema: str):
	if(isinstance(path, str)):
		path = Path(path)
	
	raise NotImplementedError('Validate is not implemented')

@dataclass
class fssNode:
	name: str
	parent: Optional['fssNode'] = None

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
