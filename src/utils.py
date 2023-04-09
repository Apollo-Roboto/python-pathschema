from fss import fssNode

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

	if(node.is_dir):
		decorator += '📁 '
	else:
		decorator += '📄 '

	print(decorator + node.name)
	for i, child in enumerate(node.childs):
		print_node_tree(
			child,
			depth + 1,
			is_last=(i == len(node.childs)-1)
		)
