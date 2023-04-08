import unittest
from src import fss
import tempfile
import uuid
from pathlib import Path

class TestValidate(unittest.TestCase):

	def _temp_dir(self):
		return Path(
			tempfile.gettempdir(),
			str(uuid.uuid4())
		)

	def test_validate(self):
		
		dir = self._temp_dir()

		print(dir)

		schema = "root/"

		fss.validate(path=dir, schema=schema)
		# self.assertEqual('foo'.upper(), 'FOO')
