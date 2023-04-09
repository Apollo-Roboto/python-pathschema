import logging
import sys

from fss import fssNode
from utils import print_node_tree

logging.basicConfig(
	stream=sys.stdout,
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S',
	format='%(levelname)s [ %(asctime)s ] %(name)s : %(message)s',
)

log = logging.getLogger(__name__)

def main():

	sample_schema = """
	Assets/
		Globals/
			Materials/
			Textures/
			Models/
			Scripts/
			Animations/
		Prefabs/
			Object1/
				Materials/
				Textures/
				Models/
				Scripts/
				Animations/
			Object2/
		CommunityAssets/
		Scenes/
	"""

	test_node_tree = fssNode(name='Assets/', childs=[
		fssNode(name='Globals/', childs=[
			fssNode(name='Materials/'),
			fssNode(name='Textures/'),
			fssNode(name='Models/'),
			fssNode(name='Scripts/'),
			fssNode(name='Animations/'),
		]),
		fssNode(name='Prefabs/'),
		fssNode(name='Prefabs/'),
		fssNode(name='CommunityAssets/'),
		fssNode(name='Scenes/'),
	])

	print_node_tree(test_node_tree)
	

if __name__ == '__main__':
	main()
