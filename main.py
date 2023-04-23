from fss.validator import Validator
from fss.exceptions import ValidationError
import os
from colorama import Fore, Back, Style


def main():

	schema = ''

	with open('./test_schema_2.txt', 'r') as f:
		schema = f.read()

	path_errors = Validator().validate('./test_directory', schema)

	print_results_1(path_errors)

	exit(0)
	exit(1)

def print_results_1(error_by_path):
	for path, errors in error_by_path.items():
		if(len(errors) > 0 ):
			print(Fore.RED + Style.BRIGHT, end='')
		else:
			print(Fore.GREEN, end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}{Style.BRIGHT}\t{error}{Style.RESET_ALL}')

def print_results_2(error_by_path):
	for path, errors in error_by_path.items():
		if(len(errors) > 0 ):
			print('🔴 ', end='')
		else:
			print('🟢 ', end='')

		print(f'{path}')

		for error in errors:
			print(f'{Fore.RED}\t{error}{Style.RESET_ALL}')

if __name__ == '__main__':
	main()
