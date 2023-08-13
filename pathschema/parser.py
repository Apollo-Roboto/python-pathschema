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

	def _detect_indentation(self, schema: str) -> str:
		for line in schema.split('\n'):

			# ignore empty lines
			if not line.strip():
				continue
			
			leading_whitespace = len(line) - len(line.lstrip())

			# impossible to evaluate if no leading whitespace, continue to next line
			if leading_whitespace == 0:
				continue
			
			# indentation is tabs
			if line.startswith('\t'):
				return '\t' * leading_whitespace
			
			# indentation is spaces
			if line.startswith(' '):
				return ' ' * leading_whitespace
		
		# if not evaluated, assume default
		return self.indentation_token

	def _indentation_count(self,  string: str, line_num: int) -> int:
		"""Counts the indentation at the beginning of a string using the indentation token"""
		tmp_str = string
		count = 0
		
		while tmp_str.startswith(self.indentation_token):
			count += 1
			tmp_str = tmp_str[len(self.indentation_token):]

		# if there is still some whitespace
		# can happen if indentation token is 4 space and there are 3 spaces instead
		if len(tmp_str) > len(tmp_str.lstrip()):
			raise SchemaError('Inconsistent indentation.', line_num)
		
		return count

	def schema_to_node_tree(self, schema: str) -> DirPathNode:

		self.indentation_token = self._detect_indentation(schema)

		root_node: DirPathNode = DirPathNode(name='schema_root')

		current_node = root_node
		node_depth = 0
		last_indentation = 0

		for line_num, line in enumerate(schema.split('\n')):
			name = line.strip()
			if len(name) == 0:
				continue

			# comments get ignored
			if name.startswith(self.comment_token):
				continue

			indentation = self._indentation_count(line, line_num+1)

			if indentation > last_indentation + 1:
				raise SchemaError('Inconsistent indentation.', line_num+1)

			last_indentation = indentation

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
