import unittest
from pathschema.validator import Validator
import tempfile
import uuid
from pathlib import Path
import os
import shutil
from pathschema.models import ValidationResult

class TestValidator(unittest.TestCase):

	@classmethod
	def tearDownClass(cls):

		# remove the temporary test directory
		shutil.rmtree(Path(
			tempfile.gettempdir(),
			'pathschema_test',
		))

	@classmethod
	def _temp_dir(cls) -> Path:
		"""Get a temporary directory"""
		return Path(
			tempfile.gettempdir(),
			'pathschema_test',
			str(uuid.uuid4())
		)

	def setUp(self) -> None:
		"""Adds a little newline to read the output better"""
		print()

	def assert_validation_result_has_errors(self, result: ValidationResult):
		self.assertTrue(result.has_error(), 'validation results did not had errors')

	def assert_validation_result_has_no_errors(self, result: ValidationResult):
		self.assertFalse(result.has_error(), f'validation results had errors: {result.errors_by_path}')

	def test_validate_path_does_not_exists(self):
		with self.assertRaises(ValueError) as e:
			Validator().validate('/should_not_exists/', schema='')
		self.assertEqual(str(e.exception), 'The path does not exists')

	def test_validate_path_is_not_a_dir(self):

		temp_file = Path(self._temp_dir(), 'test.txt')

		os.makedirs(temp_file.parent)
		temp_file.touch()

		with self.assertRaises(ValueError) as e:
			Validator().validate(temp_file, schema='')
		self.assertEqual(str(e.exception), 'The path to validate must be a directory')

	def test_validate_single_dir_pass(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('root'))

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_single_dir_fail(self):
		schema = "root/"

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate.joinpath('should_fail'))

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_dir_only_simple_pass(self):
		schema =  'Assets/\n'
		schema += '  Globals/\n'
		schema += '    Materials/\n'
		schema += '    Textures/\n'
		schema += '    Models/\n'
		schema += '    Scripts/\n'
		schema += '    Animations/\n'
		schema += '  Prefabs/\n'
		schema += '  CommunityAssets/\n'
		schema += '  Scenes/\n'

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate / 'Assets')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Materials')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Textures')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Models')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Scripts')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Animations')
		os.makedirs(dir_to_validate / 'Assets' / 'Prefabs')
		os.makedirs(dir_to_validate / 'Assets' / 'CommunityAssets')
		os.makedirs(dir_to_validate / 'Assets' / 'Scenes')

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_dir_only_simple_fail(self):
		schema =  'Assets/\n'
		schema += '  Globals/\n'
		schema += '    Materials/\n'
		schema += '    Textures/\n'
		schema += '    Models/\n'
		schema += '    Scripts/\n'
		schema += '    Animations/\n'
		schema += '  Prefabs/\n'
		schema += '  CommunityAssets/\n'
		schema += '  Scenes/\n'

		dir_to_validate = self._temp_dir()

		os.makedirs(dir_to_validate / 'Assets')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Wrong')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Textures')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Models')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Scripts')
		os.makedirs(dir_to_validate / 'Assets' / 'Globals' / 'Animations')
		os.makedirs(dir_to_validate / 'Assets' / 'Prefabs')
		os.makedirs(dir_to_validate / 'Assets' / 'Wrong')
		os.makedirs(dir_to_validate / 'Assets' / 'Scenes')

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_dir_and_files_simple_pass(self):
		schema =  'Textures/\n'
		schema += '  robot.png\n'
		schema += 'Models/\n'
		schema += '  robot.fbx\n'

		dir_to_validate = self._temp_dir()

		texture_dir = dir_to_validate.joinpath('Textures')
		os.makedirs(texture_dir)
		(texture_dir / 'robot.png').touch()

		models_dir = dir_to_validate.joinpath('Models')
		os.makedirs(models_dir)
		(models_dir / 'robot.fbx').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_dir_and_files_simple_fail(self):
		schema =  'Textures/\n'
		schema += '  robot.png\n'
		schema += 'Models/\n'
		schema += '  robot.fbx\n'

		dir_to_validate = self._temp_dir()

		texture_dir = dir_to_validate.joinpath('Textures')
		os.makedirs(texture_dir)
		(texture_dir / 'robot.png').touch()

		models_dir = dir_to_validate.joinpath('Models')
		os.makedirs(models_dir)
		(models_dir / 'robot.fbx').touch()

		os.makedirs(texture_dir / 'invalid_dir')

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_star_file_pass(self):
		schema =  'Notes/\n'
		schema += '  *\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		(note_dir / 'robot.md').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_regex_file_pass(self):
		schema =  'Notes/\n'
		schema += '  ".*\\.md"\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		(note_dir / 'robot.md').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_regex_file_fail(self):
		schema =  'Notes/\n'
		schema += '  ".*\\.md"\n'

		dir_to_validate = self._temp_dir()

		note_dir = dir_to_validate.joinpath('Notes')
		os.makedirs(note_dir)
		(note_dir / 'robot.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_star_dir_pass(self):
		schema =  'Notes/\n'
		schema += '  */\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', 'Things')
		os.makedirs(dirs)

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_regex_dir_pass(self):
		schema =  'Notes/\n'
		schema += '  "\\d+"/\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', '123456')
		os.makedirs(dirs)

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_regex_dir_fail(self):
		schema =  'Notes/\n'
		schema += '  "\\d"/\n'

		dir_to_validate = self._temp_dir()

		dirs = dir_to_validate.joinpath('Notes', 'abcde')
		os.makedirs(dirs)

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_star_and_dir_pass(self):
		schema =  'Assets/\n'
		schema += '  Textures/\n'
		schema += '    ".*\\.png"\n'
		schema += '  Models/\n'
		schema += '    ".*\\.fbx"\n'
		schema += '  *\n'

		dir_to_validate = self._temp_dir()

		assets_dir = dir_to_validate / 'Assets'
		os.makedirs(assets_dir)
		textures_dir = assets_dir / 'Textures'
		os.makedirs(textures_dir)
		models_dir = assets_dir / 'Models'
		os.makedirs(models_dir)

		(textures_dir / 'robot.png').touch()
		(models_dir / 'robot.fbx').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_star_and_dir_fail(self):
		schema =  'Assets/\n'
		schema += '  Textures/\n'
		schema += '    ".*\\.png"\n'
		schema += '  Models/\n'
		schema += '    ".*\\.fbx"\n'
		schema += '  *\n'

		dir_to_validate = self._temp_dir()

		assets_dir = dir_to_validate / 'Assets'
		os.makedirs(assets_dir)
		textures_dir = assets_dir / 'Textures'
		os.makedirs(textures_dir)
		models_dir = assets_dir / 'Models'
		os.makedirs(models_dir)

		(textures_dir / 'robot.jpg').touch()
		(models_dir / 'robot.obj').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_any_pass(self):
		schema =  'Assets/\n'
		schema += '  ...\n'

		dir_to_validate = self._temp_dir()

		assets_dir = dir_to_validate / 'Assets'
		os.makedirs(assets_dir)
		textures_dir = assets_dir / 'Textures'
		os.makedirs(textures_dir)
		models_dir = assets_dir / 'Models'
		os.makedirs(models_dir)

		(textures_dir / 'robot.png').touch()
		(models_dir / 'robot.fbx').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_pattern_star_pass(self):
		schema =  'Assets/\n'
		schema += '  Textures/\n'
		schema += '    *.png\n'

		dir_to_validate = self._temp_dir()

		assets_dir = dir_to_validate / 'Assets'
		os.makedirs(assets_dir)
		textures_dir = assets_dir / 'Textures'
		os.makedirs(textures_dir)

		(textures_dir / 'robot.png').touch()
		(textures_dir / 'planet.png').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_pattern_star_fail(self):
		schema =  'Assets/\n'
		schema += '  Textures/\n'
		schema += '    *.png\n'

		dir_to_validate = self._temp_dir()

		assets_dir = dir_to_validate / 'Assets'
		os.makedirs(assets_dir)
		textures_dir = assets_dir / 'Textures'
		os.makedirs(textures_dir)

		(textures_dir / 'robot.jpg').touch()
		(textures_dir / 'planet.jpeg').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_pattern_question_mark_pass(self):
		schema =  'Folder/\n'
		schema += '  File_?.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'File_0.txt').touch()
		(folder_dir / 'File_1.txt').touch()
		(folder_dir / 'File_2.txt').touch()
		(folder_dir / 'File_A.txt').touch()
		(folder_dir / 'File_B.txt').touch()
		(folder_dir / 'File_C.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_pattern_question_mark_fail(self):
		schema =  'Folder/\n'
		schema += '  File_?.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'Fails_00.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_forbiden_pass(self):
		schema =  'Folder/\n'
		schema += '  -File.txt\n'
		schema += '  AnAcceptableFile.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'AnAcceptableFile.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_forbiden_fail(self):
		schema =  'Folder/\n'
		schema += '  -File.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'File.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_forbiden_with_start_fail(self):
		schema =  'Folder/\n'
		schema += '  -File.txt\n'
		schema += '  *.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'File.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_forbiden_with_start2_fail(self):
		schema =  'Folder/\n'
		schema += '  *.txt\n'
		schema += '  -File.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'File.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_required_pass(self):
		schema =  'Folder/\n'
		schema += '  +File.txt\n'
		schema += '  SomeOtherFile.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'File.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_no_errors(result)

	def test_validate_required_fail(self):
		schema =  'Folder/\n'
		schema += '  +File.txt\n'
		schema += '  SomeOtherFile.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'SomeOtherFile.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_required_with_start_fail(self):
		schema =  'Folder/\n'
		schema += '  +File.txt\n'
		schema += '  *.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'SomeOtherFile.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)

	def test_validate_required_with_start2_fail(self):
		schema =  'Folder/\n'
		schema += '  *.txt\n'
		schema += '  +File.txt\n'

		dir_to_validate = self._temp_dir()

		folder_dir = dir_to_validate / 'Folder'
		os.makedirs(folder_dir)

		(folder_dir / 'SomeOtherFile.txt').touch()

		result = Validator().validate(dir_to_validate, schema)
		self.assert_validation_result_has_errors(result)
