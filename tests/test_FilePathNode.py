import unittest
from pathschema.models import FilePathNode



class TestFilePathNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_fssFileNode_eq_true(self):
		node1 = FilePathNode(name='test')
		node2 = FilePathNode(name='test')

		self.assertEqual(node1, node2)

	def test_fssFileNode_eq_false(self):
		node1 = FilePathNode(name='test')
		node2 = FilePathNode(name='tset')
		
		self.assertNotEqual(node1, node2)
