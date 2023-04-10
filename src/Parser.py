from src.fss import fssDirNode, fssFileNode, fssNode
from src.exceptions import SchemaException



class Parser():

	indentation_token = '\t'

	def _detect_indentation(self):
		raise NotImplementedError()

	def _indentation_count(self,  s: str):
		num_of_indentation = 0
		for c in s:
			if(c == self.indentation_token):
				num_of_indentation += 1
			else:
				break

		return num_of_indentation

	def schema_to_node_tree(self, schema: str) -> fssDirNode:

		root_node: fssDirNode = fssDirNode(name='schema_root')

		current_node = root_node
		node_depth = 0

		for line_num, line in enumerate(schema.split('\n')):
			indentation = self._indentation_count(line)
			name = line.strip()
			if(len(name) == 0):
				continue

			# add node
			if(indentation == node_depth):

				if(name.endswith('/')):
					node = fssDirNode(
						name=name.removesuffix('/'),
						parent=current_node,
					)
					current_node.childs.append(node)
				else:
					node = fssFileNode(
						name=name,
						parent=current_node,
					)
					current_node.childs.append(node)

			# dive in
			elif(indentation > node_depth):
		
				if(len(current_node.childs) != 0):
					current_node = current_node.childs[-1]
				node_depth += 1

				if(isinstance(current_node, fssFileNode)):
					raise SchemaException(f'Files cannot have childs. At line {line_num + 1}')

				if(name.endswith('/')):
					node = fssDirNode(
						name=name.removesuffix('/'),
						parent=current_node,
					)
					current_node.childs.append(node)
				else:
					node = fssFileNode(
						name=name,
						parent=current_node,
					)
					current_node.childs.append(node)

			# back out
			else:
				while(indentation < node_depth):
					current_node = current_node.parent
					node_depth -= 1

				if(name.endswith('/')):
					node = fssDirNode(
						name=name.removesuffix('/'),
						parent=current_node,
					)
					current_node.childs.append(node)
				else:
					node = fssFileNode(
						name=name,
						parent=current_node,
					)
					current_node.childs.append(node)

		return root_node
