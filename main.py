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

	schema =  'Assets/\n'
	schema += '\tGlobals/\n'
	schema += '\t\tMaterials/\n'
	schema += '\t\tTextures/\n'
	schema += '\t\t\t*\n'
	schema += '\t\tModels/\n'
	schema += '\t\tScripts/\n'
	schema += '\t\tAnimations/\n'
	schema += '\tPrefabs/\n'
	schema += '\tNotes.md\n'
	schema += '\tCommunityAssets/\n'
	schema += '\tScenes/\n'

	# parsed_tree =  Parser().schema_to_node_tree(schema)
	
	# print_node_tree(parsed_tree)

	try:
		Validator().validate('./test_directory', schema)
		print('valid')
	except ValidationError as e:
		print('invalid')

if __name__ == '__main__':
	main()
