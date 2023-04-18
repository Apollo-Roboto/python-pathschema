from fss.fss import fssDirNode, fssFileNode, fssNode
from fss.exceptions import SchemaError



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
				pass

			# dive in
			elif(indentation > node_depth):
		
				if(isinstance(current_node, fssDirNode) and len(current_node.childs) != 0):
					current_node = current_node.childs[-1]
				node_depth += 1

			# back out
			else:
				while(indentation < node_depth):
					if(current_node != None):
						current_node = current_node.parent
					else:
						raise Exception('Unexpected None value')
					node_depth -= 1

			if(name.endswith('/')):
				node = fssDirNode(
					name=name.removesuffix('/'),
					parent=current_node,
				)
				if(isinstance(current_node, fssDirNode)):
					current_node.childs.append(node)
				else:
					raise SchemaError(f'Files cannot have childs. At line {line_num + 1}')
			else:
				node = fssFileNode(
					name=name,
					parent=current_node,
				)
				if(isinstance(current_node, fssDirNode)):
					current_node.childs.append(node)
				else:
					raise SchemaError(f'Files cannot have childs. At line {line_num + 1}')

		return root_node
