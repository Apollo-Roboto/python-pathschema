from fss.fss import fssNode, fssFileNode, fssDirNode

def print_node_tree(node: fssNode, sort=False, _depth=0, _is_last=False, _floating=0):
	"""
	Print a visual representation of the node tree.
	"""

	decorator = ''
	for i in range(_depth):
		if i == _depth-1:
			if(_is_last):
				decorator += '└─ '
			else:
				decorator += '├─ '
		else:
			if(i >= _floating):
				decorator += '│  '
			else:
				decorator += '   '

	if(isinstance(node, fssDirNode)):
		decorator += '📁 '
		print(decorator + node.name + '/')
	else:
		decorator += '📄 '
		print(decorator + node.name)

	if(isinstance(node, fssFileNode)):
		return
	
	childs = node.childs
	if(sort == True):
		childs = sorted(childs, key=lambda x: x.name)

	for i, child in enumerate(childs):
		print_node_tree(
			child,
			_depth=_depth + 1,
			_is_last=(i == len(node.childs)-1),
			sort=sort,
			_floating = (_floating + 1) if _is_last else _floating
		)
