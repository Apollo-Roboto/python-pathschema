from fss.validator import Validator
from fss.fss import ValidationResult
import os
from colorama import Fore, Back, Style



def main():

	schema = ''

	with open('./test_schema.txt', 'r') as f:
		schema = f.read()

	result = Validator().validate('./test_directory_fail', schema)

	print_results_3(result)

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

def print_results_3(results: ValidationResult):
	for path, errors in results.errors_by_path.items():
		if(len(errors) > 0 ):
			print(f'{Fore.RED}FAIL  ', end='')
		else:
			print(f'  OK  ', end='')

		print(f'{path}{Style.RESET_ALL}')

		for error in errors:
			print(f'{Fore.RED}\t{error}{Style.RESET_ALL}')
	
	print()

	if(results.has_error()):
		print(f'{Fore.RED}{Style.BRIGHT}Invalid{Style.RESET_ALL}')
	else:
		print(f'{Fore.GREEN}{Style.BRIGHT}Valid{Style.RESET_ALL}')

if __name__ == '__main__':
	main()
