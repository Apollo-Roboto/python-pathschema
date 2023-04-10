import unittest
from src import fss
import tempfile
import uuid
from pathlib import Path
import os
import shutil

class TestValidate(unittest.TestCase):

	@classmethod
	def tearDownClass(cls):
		shutil.rmtree(Path(
			tempfile.gettempdir(),
			'python_test',
		))

	@classmethod
	def _temp_dir(cls):
		return Path(
			tempfile.gettempdir(),
			'python_test',
			str(uuid.uuid4())
		)

	def test_validate_simple_single_dir_pass(self):
		schema = "root/"

		dir = self._temp_dir()
		dir = dir.joinpath('root')

		os.makedirs(dir)

		fss.validate(dir, schema)

	def test_validate_simple_single_dir_fail(self):
		schema = "root/"

		dir = self._temp_dir()
		dir = dir.joinpath('should-fail')

		os.makedirs(dir)

		with self.assertRaises(Exception):
			fss.validate(dir, schema)
