import unittest
from pathschema.models import DirPathNode, FilePathNode, AnyPathNode, Necessity
from pathschema.parser import Parser
from pathschema.utils import print_node_tree
from pathschema.exceptions import SchemaError



class TestParse(unittest.TestCase):

	def setUp(self) -> None:
		"""Adds a little newline to read the output better"""
		print()

	def tearDown(self) -> None:
		"""Adds a little newline to read the output better"""
		print()
	
	def test_schema_to_node_tree_simple_dir_pass(self):
		schema = 'Assets/'

		root_node = Parser().schema_to_node_tree(schema)
		
		self.assertIn(DirPathNode(name='Assets', parent=root_node), root_node.childs)

	def test_schema_to_node_tree_simple_file_pass(self):
		schema = 'picture.png'

		root_node = Parser().schema_to_node_tree(schema)
		
		self.assertIn(FilePathNode(name='picture.png', parent=root_node), root_node.childs)

	def test_schema_to_node_tree_complex_dir_pass(self):
		schema =  'Assets/\n'
		schema += '  Globals/\n'
		schema += '    Materials/\n'
		schema += '    Textures/\n'
		schema += '    Models/\n'
		schema += '    Scripts/\n'
		schema += '    Animations/\n'
		schema += '  Prefabs/\n'
		schema += '  CommunityAssets/\n'
		schema += '  Scenes/\n'

		returned_tree = Parser().schema_to_node_tree(schema)
		
		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(DirPathNode(name='Globals')
					.add_child(DirPathNode(name='Materials'))
					.add_child(DirPathNode(name='Textures'))
					.add_child(DirPathNode(name='Models'))
					.add_child(DirPathNode(name='Scripts'))
					.add_child(DirPathNode(name='Animations'))
				)
				.add_child(DirPathNode(name='Prefabs'))
				.add_child(DirPathNode(name='CommunityAssets'))
				.add_child(DirPathNode(name='Scenes'))
			)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_complex_dir_and_files_pass(self):
		schema =  'Textures/\n'
		schema +=  '  robot.png\n'
		schema +=  'Models/\n'
		schema +=  '  robot.fbx\n'

		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Textures')
				.add_child(FilePathNode(name='robot.png'))
			) \
			.add_child(DirPathNode(name='Models')
				.add_child(FilePathNode(name='robot.fbx'))
			)
		
		print_node_tree(expected_tree)
		print_node_tree(returned_tree)
		
		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_file_with_child_exception(self):
		schema =  'Assets/\n'
		schema += '  file.txt\n'
		schema += '    oh_no.txt\n'

		with self.assertRaises(SchemaError) as e:
			Parser().schema_to_node_tree(schema)
		self.assertRegex(str(e.exception), r'Files cannot have childs. \(.+ line \d+\)')

	def test_schema_to_node_tree_all_pass(self):
		schema =  'Assets/\n'
		schema += '  ...\n'

		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(AnyPathNode())
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_forbiden_pass(self):
		schema =  'Assets/\n'
		schema += '  -*.md\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.md', necessity=Necessity.FORBIDDEN))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_required_pass(self):
		schema =  'Assets/\n'
		schema += '  +*.md\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.md', necessity=Necessity.REQUIRED))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_comment_ignored_pass(self):
		schema =  'Assets/\n'
		schema += '  # comment!\n'
		schema += '  *.txt\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_two_space_indentation_pass(self):
		schema =  'Assets/\n'
		schema += '  *.txt\n'
		schema += '  Textures/\n'
		schema += '    *.png\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
				.add_child(DirPathNode(name='Textures')
					.add_child(FilePathNode(name='*.png'))
				)
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_four_space_indentation_pass(self):
		schema =  'Assets/\n'
		schema += '    *.txt\n'
		schema += '    Textures/\n'
		schema += '        *.png\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
				.add_child(DirPathNode(name='Textures')
					.add_child(FilePathNode(name='*.png'))
				)
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)
		
	def test_schema_to_node_tab_indentation_pass(self):
		schema =  'Assets/\n'
		schema += '\t*.txt\n'
		schema += '\tTextures/\n'
		schema += '\t\t*.png\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
				.add_child(DirPathNode(name='Textures')
					.add_child(FilePathNode(name='*.png'))
				)
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_indentation_empty_line_pass(self):
		schema =  'Assets/\n'
		schema += '  *.txt\n'
		schema += '  Textures/\n'
		schema += '    *.png\n'
		schema += '\n'
		schema += '    *.jpg\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
				.add_child(DirPathNode(name='Textures')
					.add_child(FilePathNode(name='*.png'))
					.add_child(FilePathNode(name='*.jpg'))
				)
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_inconsistent_indentation_one_fail(self):
		"""Uses 4 spaces instead of 2"""
		schema =  'Assets/\n'
		schema += '  *.txt\n'
		schema += '  Textures/\n'
		schema += '      *.png\n'
		schema += '      *.jpg\n'
		
		with self.assertRaises(SchemaError) as e:
			Parser().schema_to_node_tree(schema)
		self.assertRegex(str(e.exception), r'Inconsistent indentation. \(.+ line \d+\)')

	def test_schema_to_node_inconsistent_indentation_two_fail(self):
		"""Uses 3 spaces instead of 2"""
		schema =  'Assets/\n'
		schema += '  *.txt\n'
		schema += '  Textures/\n'
		schema += '     *.png\n'
		schema += '     *.jpg\n'
		
		with self.assertRaises(SchemaError) as e:
			Parser().schema_to_node_tree(schema)
		self.assertRegex(str(e.exception), r'Inconsistent indentation. \(.+ line \d+\)')
