import unittest
from fss.fss import fssNode, fssDirNode, fssFileNode



class TestFssNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_fssFileNode_eq_true(self):
		node1 = fssFileNode(name='test')
		node2 = fssFileNode(name='test')

		self.assertEqual(node1, node2)

	def test_fssFileNode_eq_false(self):
		node1 = fssFileNode(name='test')
		node2 = fssFileNode(name='tset')
		
		self.assertNotEqual(node1, node2)
