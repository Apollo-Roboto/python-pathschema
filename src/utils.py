from fss import fssNode, fssFileNode, fssDirNode

def print_node_tree(node: fssNode, depth = 0, is_last = False):

	decorator = ''
	for i in range(depth):
		if i == depth-1:
			if(is_last):
				decorator += '└─ '
			else:
				decorator += '├─ '
		else:
			decorator += '│  '

	if(isinstance(node, fssDirNode)):
		decorator += '📁 '
		print(decorator + node.name + '/')
	else:
		decorator += '📄 '
		print(decorator + node.name)

	if(isinstance(node, fssFileNode)):
		return
	
	for i, child in enumerate(node.childs):
		print_node_tree(
			child,
			depth + 1,
			is_last=(i == len(node.childs)-1)
		)
