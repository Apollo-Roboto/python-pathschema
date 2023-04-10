import unittest
from fss.fss import fssDirNode, fssFileNode, fssNode
from fss.Parser import Parser
from fss.exceptions import SchemaError
import tempfile
import uuid
from pathlib import Path
import os
import shutil



class TestParse(unittest.TestCase):
	
	def test_schema_to_node_tree_simple_dir_pass(self):
		schema = 'Assets/'

		root_node = Parser().schema_to_node_tree(schema)
		
		self.assertIn(fssDirNode(name='Assets', parent=root_node), root_node.childs)

	def test_schema_to_node_tree_simple_file_pass(self):
		schema = 'picture.png'

		root_node = Parser().schema_to_node_tree(schema)
		
		self.assertIn(fssFileNode(name='picture.png', parent=root_node), root_node.childs)

	def test_schema_to_node_tree_complex_pass(self):
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

	def test_schema_to_note_tree_file_with_child_exception(self):
		schema =  'Assets/\n'
		schema += '\tfile.txt\n'
		schema += '\t\toh_no.txt\n'

		with self.assertRaises(SchemaError):
			Parser().schema_to_node_tree(schema)
