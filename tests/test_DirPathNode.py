import unittest
from pathschema.models import PathNode, DirPathNode



class TestDirPathNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_add_child_pass(self):
		parent_node = DirPathNode(name='parent')
		count = 50

		for i in range(count):
			name = 'child_' + str(i)
			parent_node.add_child(DirPathNode(name=name))

		self.assertEqual(len(parent_node.childs), count)

	def test_get_child_by_name_present_pass(self):
		node = DirPathNode(name='schema_root')
		expected_node = PathNode(name='findme')

		node.add_child(PathNode(name='node1'))
		node.add_child(PathNode(name='node2'))
		node.add_child(PathNode(name='node3'))
		node.add_child(expected_node)
		node.add_child(PathNode(name='node4'))
		node.add_child(PathNode(name='node5'))
		
		returned_node = node.get_child_by_name('findme')

		self.assertEqual(returned_node, expected_node)

	def test_get_child_by_name_missing_pass(self):
		node = DirPathNode(name='schema_root')

		node.add_child(PathNode(name='node1'))
		node.add_child(PathNode(name='node2'))
		node.add_child(PathNode(name='node3'))
		node.add_child(PathNode(name='node4'))
		node.add_child(PathNode(name='node5'))
		
		returned_node = node.get_child_by_name('findme')

		self.assertIsNone(returned_node)

	def test_fssDirNode_eq_true(self):
		node1 = DirPathNode(name='test')
		node2 = DirPathNode(name='test')

		self.assertEqual(node1, node2)

	def test_fssDirNode_eq_false(self):
		node1 = DirPathNode(name='test')
		node2 = DirPathNode(name='tset')
		
		self.assertNotEqual(node1, node2)

	def test_fssDirNode_eq_childs_true(self):
		parent_node = DirPathNode(name='parent')
		child_node = PathNode(name='child')
		node1 = DirPathNode(name='test', parent=parent_node, childs=[child_node])
		node2 = DirPathNode(name='test', parent=parent_node, childs=[child_node])

		self.assertEqual(node1, node2)

	def test_fssDirNode_eq_childs_false(self):
		parent_node = DirPathNode(name='parent')
		child_node1 = PathNode(name='child1')
		child_node2 = PathNode(name='child2')
		node1 = DirPathNode(name='test', parent=parent_node, childs=[child_node1])
		node2 = DirPathNode(name='test', parent=parent_node, childs=[child_node2])

		self.assertNotEqual(node1, node2)

	def test_fssDirNode_eq_tree_true(self):
		tree1 = DirPathNode(name='schema_root') \
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
		
		tree2 = DirPathNode(name='schema_root') \
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
		
		self.assertEqual(tree1, tree2)
