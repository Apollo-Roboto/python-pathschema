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
		schema += '\tGlobals/\n'
		schema += '\t\tMaterials/\n'
		schema += '\t\tTextures/\n'
		schema += '\t\tModels/\n'
		schema += '\t\tScripts/\n'
		schema += '\t\tAnimations/\n'
		schema += '\tPrefabs/\n'
		schema += '\tCommunityAssets/\n'
		schema += '\tScenes/\n'

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
		schema +=  '\trobot.png\n'
		schema +=  'Models/\n'
		schema +=  '\trobot.fbx\n'

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
		schema += '\tfile.txt\n'
		schema += '\t\toh_no.txt\n'

		with self.assertRaises(SchemaError) as e:
			Parser().schema_to_node_tree(schema)
		self.assertRegex(str(e.exception), r'Files cannot have childs. \(.+ line \d+\)')

	def test_schema_to_node_tree_all_pass(self):
		schema =  'Assets/\n'
		schema += '\t...\n'

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
		schema += '\t-*.md\n'
		
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
		schema += '\t+*.md\n'
		
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
		schema += '\t# comment!\n'
		schema += '\t*.txt\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = DirPathNode(name='schema_root') \
			.add_child(DirPathNode(name='Assets')
				.add_child(FilePathNode(name='*.txt'))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)
