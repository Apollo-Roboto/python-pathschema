# File System Schema

# How to use

```python
from pathschema.validator import Validator

schema = "root/"

path_to_validate = './path'

result = Validator().validate(path_to_validate, schema)

if(result.has_error()):
	print('Invalid')
else:
	print('Valid')
```

|  Symbol | Description  |
|:-------:|--------------|
| `/` | Slashes at the end of the name marks this element as a folder
| `*` | Allows files with any name
| `*/` | Allows folder with any name
| `"regex"` | Quotes adds regex validation to the file name
| `"regex"/` | Quotes with a slash adds regex validation to the folder name
| `*.ext` | Unix style pattern matching for files
| `*.ext/` | Unix style pattern matching for folders
| `...` | Allows any (and nested) files and folder
| `+` | Makes the file required
| `-` | Makes the file forbidden

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
