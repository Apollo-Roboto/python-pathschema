import unittest
from fss.Validator import Validator
from fss.exceptions import ValidationError
import tempfile
import uuid
from pathlib import Path
import os
import shutil

class TestValidator(unittest.TestCase):

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
			Validator().validate('/should_not_exists/', schema='')
		self.assertEqual(str(e.exception), 'The path does not exists')

	def test_validate_path_is_not_a_dir(self):

		temp_file = Path(self._temp_dir(), 'test.txt')

		os.makedirs(temp_file.parent)
		with open(temp_file, 'w') as f: pass

		with self.assertRaises(ValueError) as e:
			Validator().validate(temp_file, schema='')
		self.assertEqual(str(e.exception), 'The path to validate must be a directory')

	def test_validate_single_dir_pass(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('root'))

		Validator().validate(dir_to_validate, schema)

	def test_validate_single_dir_fail(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('should_fail'))

		with self.assertRaises(ValidationError) as e:
			Validator().validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')

	def test_validate_dir_only_simple_pass(self):
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

		Validator().validate(dir_to_validate, schema)

	def test_validate_dir_only_simple_fail(self):
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
			Validator().validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')

	def test_validate_dir_and_files_simple_pass(self):
		schema =  'Textures/\n'
		schema += '\trobot.png\n'
		schema += 'Models/\n'
		schema += '\trobot.fbx\n'

		dir_to_validate = self._temp_dir()

		texture_dir = dir_to_validate.joinpath('Textures')
		os.makedirs(texture_dir)
		with open(texture_dir / 'robot.png', 'w') as f: pass

		models_dir = dir_to_validate.joinpath('Models')
		os.makedirs(models_dir)
		with open(models_dir / 'robot.fbx', 'w') as f: pass

		Validator().validate(dir_to_validate, schema)

	def test_validate_dir_and_files_simple_fail(self):
		schema =  'Textures/\n'
		schema += '\trobot.png\n'
		schema += 'Models/\n'
		schema += '\trobot.fbx\n'

		dir_to_validate = self._temp_dir()

		texture_dir = dir_to_validate.joinpath('Textures')
		os.makedirs(texture_dir)
		with open(texture_dir / 'robot.png', 'w') as f: pass

		models_dir = dir_to_validate.joinpath('Models')
		os.makedirs(models_dir)
		with open(models_dir / 'robot.fbx', 'w') as f: pass

		os.makedirs(texture_dir / 'invalid_dir')

		with self.assertRaises(ValidationError) as e:
			Validator().validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')

	def test_validate_star_file_pass(self):
		schema =  'Notes/\n'
		schema += '\t*\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		with open(note_dir / 'robot.md', 'w') as f: pass

		Validator().validate(dir_to_validate, schema)

	def test_validate_regex_file_pass(self):
		schema =  'Notes/\n'
		schema += '\t".*\\.md"\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		with open(note_dir / 'robot.md', 'w') as f: pass

		Validator().validate(dir_to_validate, schema)

	def test_validate_regex_file_fail(self):
		schema =  'Notes/\n'
		schema += '\t".*\\.txt"\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		with open(note_dir / 'robot.md', 'w') as f: pass

		with self.assertRaises(ValidationError) as e:
			Validator().validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')

	def test_validate_star_dir_pass(self):
		schema =  'Notes/\n'
		schema += '\t*/\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', 'Things')
		os.makedirs(dirs)

		Validator().validate(dir_to_validate, schema)

	def test_validate_regex_dir_pass(self):
		schema =  'Notes/\n'
		schema += '\t"\\d+"/\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', '123456')
		os.makedirs(dirs)

		Validator().validate(dir_to_validate, schema)

	def test_validate_regex_dir_fail(self):
		schema =  'Notes/\n'
		schema += '\t"\\d"/\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', 'abcde')
		os.makedirs(dirs)

		with self.assertRaises(ValidationError) as e:
			Validator().validate(dir_to_validate, schema)
		# self.assertEqual(str(e.exception), '')
