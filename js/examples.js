
// paths:
//   first key is root folder name
//   if object -> is folder
//   if null -> is file

example_schemas = [
	{
		'name': 'Photo by years',
		'schema':
			'# folders must be a year\n' +
			'"[0-9]{4}"/\n' +
			'  *.png\n' +
			'\n' +
			'Unknown Year/\n' +
			'  *.png\n',
		'paths': {
			'photos': {
				'2020': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
				'2021': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
				'2022': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
				'2023': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
				'2024': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
				'2025': {

				},
				'2026': {

				},
				'Unknown Year': {
					'1.png': null,
					'2.png': null,
					'3.png': null,
					'4.png': null,
				},
			},
		},
	},
	{
		'name': 'Python project',
		'schema':
			'.github/\n' +
			'  ...\n' +
			'.vscode/\n' +
			'  ...\n' +
			'\n' +
			'+ src/\n' +
			'  + __init__.py\n' +
			'  + __main__.py\n' +
			'  # module format is lowercase and underscore separated\n' +
			'  "[a-z_]+"/\n' +
			'    + __init__.py\n' +
			'    "[a-z_]+.py"\n' +
			'  "[a-z_]+.py"\n' +
			'\n' +
			'+ tests/\n' +
			'  __init__.py\n' +
			'  test_*.py\n' +
			'\n' +
			'# documentation\n' +
			'doc/\n' +
			'  images/\n' +
			'    *.png\n' +
			'  *.md\n' +
			'\n' +
			'+ README.md\n' +
			'+ pyproject.toml\n' +
			'+ requirements.txt \n' +
			'\n' +
			'# accept other files\n' +
			'*\n',
		'paths': {
			'a_cool_python_project': {
				'.github': {
					'workflows': {
						'build.yml': null,
					},
				},
				'.vscode': {
					'tasks.json': null,
				},
				'src': {
					'__init__.py': null,
					'__main__.py': null,
					'models': {
						'__init__.py': null,
						'robot.py': null,
					},
				},
				'tests': {
					'test_robot.py': null
				},
				'.gitignore': null,
				'.pathschema': null,
				'.pylintrc': null,
				'LICENSE': null,
				'README.md': null,
				'pyproject.toml': null,
				'requirements.txt': null,
			},
		},
	},
]
