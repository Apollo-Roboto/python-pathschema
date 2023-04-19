import logging
import sys

from fss.fss import fssNode, fssDirNode, fssFileNode
from fss.Parser import Parser
from fss.Validator import Validator
from fss.exceptions import ValidationError
from fss.utils import print_node_tree

logging.basicConfig(
	stream=sys.stdout,
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S',
	format='%(levelname)s [ %(asctime)s ] %(name)s : %(message)s',
)

log = logging.getLogger(__name__)

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
