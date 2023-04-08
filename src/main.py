import logging
import sys
from dotenv import load_dotenv

logging.basicConfig(
	stream=sys.stdout,
	level=logging.INFO,
	datefmt='%Y-%m-%d %H:%M:%S',
	format='%(levelname)s [ %(asctime)s ] %(name)s : %(message)s',
)

log = logging.getLogger(__name__)

def main():
	load_dotenv()
	log.info("Hello World!")

if __name__ == '__main__':
	main()
