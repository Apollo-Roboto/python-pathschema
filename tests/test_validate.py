import unittest
import src.fss
import tempfile

class TestValidate(unittest.TestCase):

	def test_validate(self):
		
		# C:\Users\USER\AppData\Local\Temp
		dir = tempfile.gettempdir()

		print(dir)

		# fss.validate()
		# self.assertEqual('foo'.upper(), 'FOO')
