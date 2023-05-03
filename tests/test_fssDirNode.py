import unittest
from fss.fss import fssNode, fssDirNode, fssFileNode
from fss.utils import print_node_tree



class TestFssDirNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_add_child_pass(self):
		parent_node = fssDirNode(name='parent')
		count = 50

		for i in range(count):
			name = 'child_' + str(i)
			parent_node.add_child(fssDirNode(name=name))

		self.assertEqual(len(parent_node.childs), count)

	def test_get_child_by_name_present_pass(self):
		node = fssDirNode(name='schema_root')
		expected_node = fssNode(name='findme', parent=node)

		node.childs.append(fssNode(name='node1', parent=node))
		node.childs.append(fssNode(name='node2', parent=node))
		node.childs.append(fssNode(name='node3', parent=node))
		node.childs.append(expected_node)
		node.childs.append(fssNode(name='node4', parent=node))
		node.childs.append(fssNode(name='node5', parent=node))
		
		returned_node = node.get_child_by_name('findme')

		self.assertEqual(returned_node, expected_node)

	def test_get_child_by_name_missing_pass(self):
		node = fssDirNode(name='schema_root')

		node.childs.append(fssNode(name='node1', parent=node))
		node.childs.append(fssNode(name='node2', parent=node))
		node.childs.append(fssNode(name='node3', parent=node))
		node.childs.append(fssNode(name='node4', parent=node))
		node.childs.append(fssNode(name='node5', parent=node))
		
		returned_node = node.get_child_by_name('findme')

		self.assertIsNone(returned_node)

	def test_fssDirNode_eq_true(self):
		node1 = fssDirNode(name='test')
		node2 = fssDirNode(name='test')

		self.assertEqual(node1, node2)

	def test_fssDirNode_eq_false(self):
		node1 = fssDirNode(name='test')
		node2 = fssDirNode(name='tset')
		
		self.assertNotEqual(node1, node2)

	def test_fssDirNode_eq_childs_true(self):
		parent_node = fssDirNode(name='parent')
		child_node = fssNode(name='child')
		node1 = fssDirNode(name='test', parent=parent_node, childs=[child_node])
		node2 = fssDirNode(name='test', parent=parent_node, childs=[child_node])

		self.assertEqual(node1, node2)

	def test_fssDirNode_eq_childs_false(self):
		parent_node = fssDirNode(name='parent')
		child_node1 = fssNode(name='child1')
		child_node2 = fssNode(name='child2')
		node1 = fssDirNode(name='test', parent=parent_node, childs=[child_node1])
		node2 = fssDirNode(name='test', parent=parent_node, childs=[child_node2])

		self.assertNotEqual(node1, node2)

	def test_fssDirNode_eq_tree_true(self):
		tree1 = fssDirNode(name='schema_root') \
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
		
		tree2 = fssDirNode(name='schema_root') \
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
		
		self.assertEqual(tree1, tree2)
