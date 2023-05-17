from pathschema.models import DirPathNode, FilePathNode, AnyPathNode, Necessity
from pathschema.exceptions import SchemaError

illegalCharacters = ['\\', '/', '?', '*', ':', '|', '"', '<', '>']
# dot '.' is not allowed at the end of a directory



class Parser():
	"""Parses the path schema definition"""

	indentation_token = '\t'
	directory_token = '/'
	required_token = '+'
	forbidden_token = '-'
	any_token = '...'
	comment_token = '#'

	def _detect_indentation(self):
		raise NotImplementedError()

	def _indentation_count(self,  string: str):
		num_of_indentation = 0
		for character in string:
			if character == self.indentation_token:
				num_of_indentation += 1
			else:
				break

		return num_of_indentation

	def schema_to_node_tree(self, schema: str) -> DirPathNode:

		root_node: DirPathNode = DirPathNode(name='schema_root')

		current_node = root_node
		node_depth = 0

		for line_num, line in enumerate(schema.split('\n')):
			indentation = self._indentation_count(line)
			name = line.strip()
			if len(name) == 0:
				continue

			# comments get ignored
			if name.startswith(self.comment_token):
				continue

			# add node
			if indentation == node_depth:
				pass

			# dive in
			elif indentation > node_depth:

				if(isinstance(current_node, DirPathNode) and len(current_node.childs) != 0):
					current_node = current_node.childs[-1]
				node_depth += 1

			# back out
			else:
				while indentation < node_depth:
					if current_node is not None:
						current_node = current_node.parent
					else:
						raise Exception('Unexpected None value')
					node_depth -= 1

			necessity = Necessity.OPTIONAL

			if name.startswith(self.forbidden_token):
				name = name.removeprefix(self.forbidden_token)
				necessity = Necessity.FORBIDDEN

			elif name.startswith(self.required_token):
				name = name.removeprefix(self.required_token)
				necessity = Necessity.REQUIRED

			if name == self.any_token:
				if necessity != Necessity.OPTIONAL:
					raise SchemaError(f'Any ({self.any_token}) Cannot be forbidden or required.', line_num+1)

				node = AnyPathNode()

			elif name.endswith(self.directory_token):
				node = DirPathNode(
					name=name.removesuffix(self.directory_token).strip(),
					parent=current_node,
					necessity=necessity,
				)

			else:
				node = FilePathNode(
					name=name.strip(),
					parent=current_node,
					necessity=necessity,
				)

			if isinstance(current_node, DirPathNode):
				current_node.childs.append(node)
			else:
				raise SchemaError(f'Files cannot have childs.', line_num+1)

		return root_node
