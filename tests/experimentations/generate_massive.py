from pathlib import Path
from typing import IO, Generator
from datetime import datetime
import asyncio

schema_file_path = Path('./test_massive_schema.txt')
directory_path = Path('./test_massive_directory')

schema_file = open(schema_file_path, 'w')

def id_generator() -> Generator[str, None, None]:
	i = 0
	while(True):
		yield str(i)
		i += 1

id_gen = id_generator()

async def write_nodes(file: IO, current_depth, max_depth):
	prefix = current_depth * '\t'
	
	# normal file
	file.write(prefix + 'f' + next(id_gen) + '\n')
	# required file
	file.write(prefix + '+f' + next(id_gen) + '\n')
	# forbidden file
	file.write(prefix + '-f' + next(id_gen) + '\n')
	# required file regex
	file.write(prefix + '+"f' + next(id_gen) + '"\n')
	# forbidden file regex
	file.write(prefix + '-"f' + next(id_gen) + '"\n')
	# required file pattern
	file.write(prefix + '+f*' + next(id_gen) + '\n')
	# forbidden file pattern
	file.write(prefix + '-f*' + next(id_gen) + '\n')

	# normal folder
	file.write(prefix + 'd' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# required folder
	file.write(prefix + '+d' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# forbidden folder
	file.write(prefix + '-d' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# required folder regex
	file.write(prefix + '+"d' + next(id_gen) + '"/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# forbidden folder regex
	file.write(prefix + '-"d' + next(id_gen) + '"/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# required folder pattern
	file.write(prefix + '+d*' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	# forbidden folder pattern
	file.write(prefix + '-d*' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)

	file.write(prefix + 'd' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	file.write(prefix + 'd' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)
	file.write(prefix + 'd' + next(id_gen) + '/\n')
	if(current_depth < max_depth):
		await write_nodes(file, current_depth+1, max_depth)

async def create_path(path: Path, current_depth, max_depth):
	# normal file
	Path(path, 'f' + next(id_gen)).touch()
	# required file
	Path(path, 'f' + next(id_gen)).touch()
	# forbidden file
	Path(path, 'f' + next(id_gen)).touch()
	# required file regex
	Path(path, 'f' + next(id_gen)).touch()
	# forbidden file regex
	Path(path, 'f' + next(id_gen)).touch()
	# required file pattern
	Path(path, 'fp' + next(id_gen)).touch()
	# forbidden file pattern
	Path(path, 'fp' + next(id_gen)).touch()

	# normal folder
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# required folder
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# forbidden folder
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# required folder regex
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# forbidden folder regex
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# required folder pattern
	directory = Path(path, 'dp' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	# forbidden folder pattern
	directory = Path(path, 'dp' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)
	directory = Path(path, 'd' + next(id_gen))
	directory.mkdir()
	if(current_depth < max_depth):
		await create_path(directory, current_depth+1, max_depth)

async def main():

	time_start = datetime.now()

	id_gen = id_generator()
	await write_nodes(schema_file, 0, 5)

	schema_file.close()

	id_gen = id_generator()
	directory_path.mkdir()
	await create_path(directory_path, 0, 5)

	print('DONE')
	print(f'It took {datetime.now() - time_start}')

asyncio.run(main())