from pathschema.validator import Validator
from pathschema.models import ValidationResult
from colorama import Fore, Style
from datetime import datetime



def main():

	start_time = datetime.now()

	schema = ''
	with open('./tests/experimentations/test_schema.txt', 'r') as f:
	# with open('./tests/experimentations/test_massive_schema.txt', 'r') as f:
		schema = f.read()

	# result = Validator().validate('./tests/experimentations/test_massive_directory', schema)
	result = Validator().validate('./tests/experimentations/test_directory_ok', schema)
	# result = Validator().validate('./tests/experimentations/test_directory_fail', schema)

	print()

	print_results_3(result, errors_only=False)
	print(f'it took {datetime.now() - start_time} to complete')

	if(result.has_error()):
		exit(1)
	else:
		exit(0)

def print_results_1(results: ValidationResult):
	for path, errors in results.errors_by_path.items():
		if(len(errors) > 0 ):
			print(Fore.RED + Style.BRIGHT, end='')
		else:
			print(Fore.GREEN, end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}{Style.BRIGHT}\t{error}{Style.RESET_ALL}')

	print()

	if(results.has_error()):
		print(f'{Fore.RED}{Style.BRIGHT}Invalid{Style.RESET_ALL}')
	else:
		print(f'{Fore.GREEN}{Style.BRIGHT}Valid{Style.RESET_ALL}')

def print_results_2(results: ValidationResult):
	for path, errors in results.errors_by_path.items():
		if(len(errors) > 0 ):
			print('🔴 ', end='')
		else:
			print('🟢 ', end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}\t{error}{Style.RESET_ALL}')

	print()

	if(results.has_error()):
		print(f'{Fore.RED}{Style.BRIGHT}Invalid{Style.RESET_ALL}')
	else:
		print(f'{Fore.GREEN}{Style.BRIGHT}Valid{Style.RESET_ALL}')

def print_results_3(results: ValidationResult, errors_only=False):

	num_of_errors = 0
	num_of_path = 0

	for path, errors in results.errors_by_path.items():
		num_of_path += 1
		if(len(errors) > 0 ):
			num_of_errors += 1
			print(f'{Fore.RED}FAIL  ', end='')
		else:
			if(errors_only): continue
			print(f'  OK  ', end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}\t{error}{Style.RESET_ALL}')
	
	print()

	score = f'{num_of_path-num_of_errors}/{num_of_path}'

	if(num_of_errors > 0):
		print(f'{Fore.RED}{Style.BRIGHT}{score} Invalid{Style.RESET_ALL}')
	else:
		print(f'{Fore.GREEN}{Style.BRIGHT}{score} Valid{Style.RESET_ALL}')

if __name__ == '__main__':
	main()
