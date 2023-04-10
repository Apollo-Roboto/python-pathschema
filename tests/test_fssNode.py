import unittest
from fss.fss import fssNode
import tempfile
import uuid
from pathlib import Path
import os
import shutil

class TestFssNode(unittest.TestCase):

	def setUp(self):
		"""Adds a little newline to read the output better"""
		print()

	def test_is_regex_true(self):
		node = fssNode(name='"[0-9]+"')
		self.assertTrue(node.is_regex)

	def test_is_regex_false(self):
		node = fssNode(name='test')
		self.assertFalse(node.is_regex)

	def test_is_match_all_true(self):
		node = fssNode(name='*')
		self.assertTrue(node.is_match_all)

	def test_is_match_all_false(self):
		node = fssNode(name='test')
		self.assertFalse(node.is_match_all)

	def test_validate_against_identical_pass(self):
		params = ['test', 'name', 'document.txt']
		for name in params:
			node = fssNode(name=name)
			self.assertTrue(node.validate_against(name))

	def test_validate_against_simple_fail(self):
		node = fssNode(name='test')
		self.assertFalse(node.validate_against('should_fail'))

	def test_validate_against_star_pass(self):
		params = ['test', 'name', '0', 'hello.txt', 'model.fbx.bak']
		for name in params:
			node = fssNode(name='*')
			self.assertTrue(node.validate_against(name))

	def test_validate_against_regex_pass(self):
		params = [
			('"[0-9]+"', '0123456'),
			('".*thing.*"', 'this_is_a_thing.txt'),
			('"[a-z]+"', 'abcdefg'),
			('"test_.*"', 'test_abcdefg'),
		]
		for node_name, name in params:
			node = fssNode(name=node_name)
			self.assertTrue(node.validate_against(name), f'{node_name} did not validate against {name}')
