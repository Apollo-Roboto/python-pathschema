from colorama import Fore, Style

from pathschema.models import PathNode, FilePathNode, DirPathNode, AnyPathNode, Necessity



def print_node_tree(node: PathNode, sort=False, prefix=''):
	"""
	Print a visual representation of the node tree.
	"""

	if not isinstance(node, DirPathNode):
		return

	childs = node.childs
	if sort:
		childs = sorted(childs, key=lambda x: x.name)

	for i, child in enumerate(childs):

		color = Fore.RESET

		if child.necessity == Necessity.REQUIRED:
			color = Fore.RED + Style.BRIGHT
		elif child.necessity == Necessity.FORBIDDEN:
			color = Fore.GREEN + Style.BRIGHT

		if i == len(childs) - 1:

			if isinstance(child, DirPathNode):
				print(f'{prefix}╰── 📁 {color}{child.name}/{Style.RESET_ALL}')
				print_node_tree(child, sort, prefix + "    ")
				continue

			if isinstance(child, FilePathNode):
				print(f'{prefix}╰── 📄 {color}{child.name}{Style.RESET_ALL}')
				continue

			if isinstance(child, AnyPathNode):
				print(f'{prefix}╰── {color}{child.name}{Style.RESET_ALL}')
				continue

		else:

			if isinstance(child, DirPathNode):
				print(f'{prefix}├── 📁 {color}{child.name}/{Style.RESET_ALL}')
				print_node_tree(child, sort, prefix + "│   ")
				continue

			if isinstance(child, FilePathNode):
				print(f'{prefix}├── 📄 {color}{child.name}{Style.RESET_ALL}')
				continue

			if isinstance(child, AnyPathNode):
				print(f'{prefix}├── {color}{child.name}{Style.RESET_ALL}')
				continue
