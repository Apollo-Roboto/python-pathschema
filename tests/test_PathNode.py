import unittest
from pathschema.models import PathNode



class TestPathNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_is_regex_true(self):
		node = PathNode(name='"[0-9]+"')
		self.assertTrue(node.is_regex)

	def test_is_regex_false(self):
		node = PathNode(name='test')
		self.assertFalse(node.is_regex)

	def test_validate_against_identical_pass(self):
		params = ['test', 'name', 'document.txt']
		for name in params:
			node = PathNode(name=name)
			self.assertTrue(node.validate_against(name))

	def test_validate_against_simple_fail(self):
		node = PathNode(name='test')
		self.assertFalse(node.validate_against('should_fail'))

	def test_validate_against_star_pass(self):
		params = ['test', 'name', '0', 'hello.txt', 'model.fbx.bak']
		for name in params:
			node = PathNode(name='*')
			self.assertTrue(node.validate_against(name))

	def test_validate_against_regex_pass(self):
		params = [
			('"[0-9]+"', '0123456'),
			('".*thing.*"', 'this_is_a_thing.txt'),
			('"[a-z]+"', 'abcdefg'),
			('"test_.*"', 'test_abcdefg'),
		]
		for node_name, name in params:
			node = PathNode(name=node_name)
			self.assertTrue(node.validate_against(name), f'{node_name} did not validate against {name}')

	def test_fssNode_eq_true(self):
		node1 = PathNode(name='test')
		node2 = PathNode(name='test')

		self.assertEqual(node1, node2)

	def test_fssNode_eq_false(self):
		node1 = PathNode(name='test')
		node2 = PathNode(name='tset')
		
		self.assertNotEqual(node1, node2)

	def test_fssNode_path(self):
		node1 = PathNode(name='node1')
		node2 = PathNode(name='node2', parent=node1)
		node3 = PathNode(name='node3', parent=node2)
		node4 = PathNode(name='node4', parent=node3)
		node5 = PathNode(name='node5', parent=node4)

		self.assertEqual(node5.path, 'node1/node2/node3/node4/node5')
