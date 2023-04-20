from fss.validator import Validator
from fss.exceptions import ValidationError
import os


def main():

	schema = ''

	with open('./test_schema_1.txt', 'r') as f:
		schema = f.read()

	try:
		Validator().validate('./test_directory', schema)
		print('valid')
	except ValidationError as e:
		print('invalid')

if __name__ == '__main__':
	main()
