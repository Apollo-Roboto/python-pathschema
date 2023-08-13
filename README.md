# Path Schema

![PyPi Version](https://img.shields.io/pypi/v/pathschema.svg) ![PyPI Python Version](https://img.shields.io/pypi/pyversions/pathschema.svg?logo=python&logoColor=gold) ![License MIT](https://img.shields.io/pypi/l/pathschema)

```bash
pip install pathschema
```

[Check out the online demo!](https://apollo-roboto.github.io/python-pathschema/)

# How to use

```python
from pathschema import validate

schema = 'YOUR SCHEMA HERE'

path_to_validate = './path'

with open('path/to/schema.pathschema', 'r') as f:
	schema = f.read()

result = validate(path_to_validate, schema)

if(result.has_error()):
	print('Invalid')
else:
	print('Valid')
```

## Syntax

|  Symbol | Description  | Example |
|---------|--------------|---------|
| `/` | Slashes at the end of the name marks this path as a folder | `root/` |
| `""` | Quotes adds regex validation to the file name | `"file[0-9]{3}"` |
| `""/` | Quotes with a slash adds regex validation to the folder name | `"folder[0-9]{3}"/` |
| `*` | Unix style pattern matching for files | `*.txt` |
| `*/` | Unix style pattern matching for folders | `log_*/` |
| `...` | Allows any (and nested) files and folder | `...` |
| `+` | A `+` at the start makes the file or folder required | `+required_file.txt` |
| `-` | A `-` at the start makes the file or folder forbidden | `-forbidden_folder/` |
| `#` | Write a comment | `# cool comment` |

## Command line

pathschema can be used directly in the command line.

```bash
python -m pathschema ./.pathschema path/to/dir/to/validate
```

Argument details:
```txt
usage: __main__.py [-h] [--errors-only] schema directory

Validate a directory against a schema

positional arguments:
  schema         Path to schema file
  directory      Path to directory to validate

options:
  -h, --help     show this help message and exit
  --errors-only  Only show errors
```

# Development

Installing
```bash
python -m pip install -r ./requirements.txt
python -m build
python -m pip install -e .
```

Running tests
```bash
python -m unittest discover -v -s ./tests -p test_*.py
```

Command line without installing
```bash
python ./pathschema/ ./tests/experimentations/test_schema.pathschema ./tests/experimentations/test_directory_ok
```

# Example Schema Definition

Example:
```txt
assets/
	textures/
		*.gif
		*.png
	materials/
		"(trans|solid)_.+\.mat"
	+README.md
```

## Only allows `.mp4` or `.flv` in the `videos` folder
```txt
videos/
	*.mp4
	*.flv
```

This structure would be valid.
```txt
videos/
	robots.mp4
	planets.flv
	my-mix-tape.flv
```

This structure would be invalid. *(`.png` and `.jpg` is not allowed)*
```txt
videos/
	office.png
	robots.jpg
```

## Any files and folder allowed in the `assets` folder
```txt
assets/
	...
```

Any files and directories would be valid in the `assets` folder.
```txt
assets/
	banner.png
	backgrounds/
		bg_black.png
		bg_white.png
```

## Must have a `README.md` file
```txt
example/
	*/
		*
		+README.md
```

This structure would be valid.

```txt
example/
	things/
		file.txt
		README.md
	morethings/
		README.md
```

This structure would be invalid. (Missing `README.md`)

```txt
example/
	things/
		file.txt
	morethings/
```
