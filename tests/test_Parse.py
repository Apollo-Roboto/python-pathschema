import unittest
from fss.fss import fssDirNode, fssFileNode, fssAnyNode, Necessity
from fss.parser import Parser
from fss.utils import print_node_tree
from fss.exceptions import SchemaError



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
		
		self.assertIn(fssDirNode(name='Assets', parent=root_node), root_node.childs)

	def test_schema_to_node_tree_simple_file_pass(self):
		schema = 'picture.png'

		root_node = Parser().schema_to_node_tree(schema)
		
		self.assertIn(fssFileNode(name='picture.png', parent=root_node), root_node.childs)

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
		
		expected_tree = fssDirNode(name='schema_root') \
			.add_child(fssDirNode(name='Assets')
				.add_child(fssDirNode(name='Globals')
					.add_child(fssDirNode(name='Materials'))
					.add_child(fssDirNode(name='Textures'))
					.add_child(fssDirNode(name='Models'))
					.add_child(fssDirNode(name='Scripts'))
					.add_child(fssDirNode(name='Animations'))
				)
				.add_child(fssDirNode(name='Prefabs'))
				.add_child(fssDirNode(name='CommunityAssets'))
				.add_child(fssDirNode(name='Scenes'))
			)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_complex_dir_and_files_pass(self):
		schema =  'Textures/\n'
		schema +=  '\trobot.png\n'
		schema +=  'Models/\n'
		schema +=  '\trobot.fbx\n'

		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = fssDirNode(name='schema_root') \
			.add_child(fssDirNode(name='Textures')
				.add_child(fssFileNode(name='robot.png'))
			) \
			.add_child(fssDirNode(name='Models')
				.add_child(fssFileNode(name='robot.fbx'))
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
		self.assertRegex(str(e.exception), r'Files cannot have childs. At line \d+')

	def test_schema_to_node_tree_all_pass(self):
		schema =  'Assets/\n'
		schema += '\t...\n'

		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = fssDirNode(name='schema_root') \
			.add_child(fssDirNode(name='Assets')
				.add_child(fssAnyNode())
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_forbiden_pass(self):
		schema =  'Assets/\n'
		schema += '\t-*.md\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = fssDirNode(name='schema_root') \
			.add_child(fssDirNode(name='Assets')
				.add_child(fssFileNode(name='*.md', necessity=Necessity.FORBIDDEN))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)

	def test_schema_to_node_tree_required_pass(self):
		schema =  'Assets/\n'
		schema += '\t+*.md\n'
		
		returned_tree = Parser().schema_to_node_tree(schema)

		expected_tree = fssDirNode(name='schema_root') \
			.add_child(fssDirNode(name='Assets')
				.add_child(fssFileNode(name='*.md', necessity=Necessity.REQUIRED))
			)

		print_node_tree(expected_tree)
		print_node_tree(returned_tree)

		self.assertEqual(expected_tree, returned_tree)
