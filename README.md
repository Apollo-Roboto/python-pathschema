# File System Schema

# How to use

```python
from pathschema import validate

schema = "root/"

path_to_validate = './path'

result = validate(path_to_validate, schema)

if(result.has_error()):
	print('Invalid')
else:
	print('Valid')
```

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
