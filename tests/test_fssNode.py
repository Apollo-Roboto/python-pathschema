import unittest
from src.fss import fssNode
import tempfile
import uuid
from pathlib import Path
import os
import shutil

class TestFssNode(unittest.TestCase):

	def test_is_dir_pass(self):
		node = fssNode(name="root/")
		self.assertTrue(node.is_dir)

	def test_is_dir_fail(self):
		node = fssNode(name="notes.txt")
		self.assertFalse(node.is_dir)

	def test_is_file_pass(self):
		node = fssNode(name="notes.txt")
		self.assertTrue(node.is_file)

	def test_is_file_fail(self):
		node = fssNode(name="root/")
		self.assertFalse(node.is_file)

	def test_validate_name_dir_pass(self):
		node = fssNode(name="root/")
		self.assertTrue(node.validate_name())

	def test_validate_name_dir_fail(self):
		node = fssNode(name="ro?ot/")
		self.assertFalse(node.validate_name())

	def test_validate_name_file_pass(self):
		node = fssNode(name="notes.txt")
		self.assertTrue(node.validate_name())

	def test_validate_name_file_fail(self):
		node = fssNode(name="no?tes.txt")
		self.assertFalse(node.validate_name())
