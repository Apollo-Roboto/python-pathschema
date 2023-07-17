import argparse
from pathlib import Path
from colorama import Fore, Style

from pathschema import validate
from pathschema.models import ValidationResult
from pathschema.exceptions import SchemaError



def parse_arguments():
	parser = argparse.ArgumentParser(description="Validate a directory against a schema")
	parser.add_argument('schema', type=Path, help='Path to schema file')
	parser.add_argument('directory', type=Path, help='Path to directory to validate')
	parser.add_argument('--errors-only', action='store_true', default=False, help='Only show errors')
	return parser.parse_args()



def main(args):

	schema = ''
	with open(args.schema, 'r') as f:
		schema = f.read()

	result = None
	try:
		result = validate(args.directory, schema)
	except SchemaError as e:
		print('Error in schema definition')
		print(str(e))
		exit(1)

	print_results(result, errors_only=args.errors_only)

	if(result.has_error()):
		exit(1)
	else:
		exit(0)



def print_results(results: ValidationResult, errors_only=False):
	"""Prints the validation results to the console in a human readable way"""

	print()

	num_of_errors = 0
	num_of_path = 0

	for path, errors in results.errors_by_path.items():
		num_of_path += 1
		if(len(errors) > 0 ):
			num_of_errors += 1
			print(f'{Fore.RED}FAIL  ', end='')
		else:
			if errors_only : continue
			print('  OK  ', end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}\t{error}{Style.RESET_ALL}')

	# spacing
	print()

	score = f'{num_of_path-num_of_errors}/{num_of_path}'

	print(f'Valid paths: {score}')

	if(num_of_errors > 0):
		print(f'{Fore.RED}{Style.BRIGHT}FAILED{Style.RESET_ALL}')
	else:
		print(f'{Fore.GREEN}{Style.BRIGHT}PASSED{Style.RESET_ALL}')



if __name__ == '__main__':
	args = parse_arguments()
	main(args)
