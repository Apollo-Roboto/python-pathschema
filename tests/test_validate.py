import unittest
from fss.Validator import validate
from fss.exceptions import ValidationError
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
	
	def setUp(self) -> None:
		"""Adds a little newline to read the output better"""
		print()

	def test_validate_path_does_not_exists(self):
		with self.assertRaises(ValueError) as e:
			validate('/should_not_exists/', schema='')
		self.assertEqual(str(e.exception), 'The path does not exists')

	def test_validate_path_is_not_a_dir(self):

		temp_file = Path(self._temp_dir(), 'test.txt')

		os.makedirs(temp_file.parent)
		with open(temp_file, 'w') as f: pass

		with self.assertRaises(ValueError) as e:
			validate(temp_file, schema='')
		self.assertEqual(str(e.exception), 'The path to validate must be a directory')

	def test_validate_simple_single_dir_pass(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('root'))

		validate(dir_to_validate, schema)

	def test_validate_simple_single_dir_fail(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('should_fail'))

		with self.assertRaises(ValidationError) as e:
			validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')

	def test_validate_complex_name_only_pass(self):
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

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('Assets'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Materials'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Textures'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Models'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Scripts'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Animations'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Prefabs'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'CommunityAssets'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Scenes'))

		validate(dir_to_validate, schema)

	def test_validate_complex_name_only_fail(self):
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

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('Assets'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Wrong'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Textures'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Models'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Scripts'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Globals', 'Animations'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Prefabs'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Wrong'))
		os.makedirs(dir_to_validate.joinpath('Assets', 'Scenes'))

		with self.assertRaises(ValidationError) as e:
			validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')
