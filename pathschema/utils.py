from colorama import Fore, Style

from pathschema.models import PathNode, FilePathNode, DirPathNode, AnyPathNode, Necessity



def print_node_tree(node: PathNode, sort=False, _depth=0, _is_last=False, _floating=0):
	"""
	Print a visual representation of the node tree.
	"""

	decorator = ''
	for i in range(_depth):
		if i == _depth-1:
			if _is_last:
				decorator += '└─ '
			else:
				decorator += '├─ '
		else:
			if i >= _floating:
				decorator += '│  '
			else:
				decorator += '   '

	color = Fore.RESET
	if node.necessity == Necessity.FORBIDDEN:
		color = Fore.RED + Style.BRIGHT
	if node.necessity == Necessity.REQUIRED:
		color = Fore.GREEN + Style.BRIGHT

	if isinstance(node, DirPathNode):
		decorator += '📁 ' + color
		print(decorator + node.name + '/' + Style.RESET_ALL)
	elif isinstance(node, FilePathNode):
		decorator += '📄 ' + color
		print(decorator + node.name + Style.RESET_ALL)
	elif isinstance(node, AnyPathNode):
		decorator += '' + color
		print(decorator + node.name + Style.RESET_ALL)

	if not isinstance(node, DirPathNode):
		return

	childs = node.childs
	if sort:
		childs = sorted(childs, key=lambda x: x.name)

	for i, child in enumerate(childs):
		print_node_tree(
			child,
			_depth=_depth + 1,
			_is_last=(i == len(node.childs)-1),
			sort=sort,
			_floating = (_floating + 1) if _is_last else _floating
		)
