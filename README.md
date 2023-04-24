# File System Schema

# How to use

```python
from fss.validator import Validator

schema = "root/"

path_to_validate = './path'

result = Validator().validate(path_to_validate, schema)
if(result.has_error())
	print('Invalid')
else:
	print('Valid')
```

# Example Schema Definition

|  Symbol | Description  | Implemented |
|:-------:|--------------|:-----------:|
| `/` | Slashes at the end of the name marks this element as a folder | X | 
| `*` | Allows files with any name | X |
| `*/` | Allows folder with any name | X |
| `"regex"` | Quotes adds regex validation to the file name | X |
| `"regex"/` | Quotes with a slash adds regex validation to the folder name | X |
| `*.ext` | Unix style pattern matching for files | X |
| `*.ext/` | Unix style pattern matching for folders | X |
| `...` | Allows any (and nested) files and folder | X |
| `<0-5>` | Control the quantity of matching folders/files |   |
| `+` | Makes the file required |   |
| `-` | Makes the file forbidden |   |

```txt
assets/
	textures/
		".*(png)|(gif)$"
		*.gif
		*.png
	models/
		* [0-255]
	...
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

This structure would be valid.
```txt
assets/
	banner.png
	backgrounds/
		bg_black.png
		bg_white.png
```

This structure would be invalid. *(it's missing an `s`)*
```txt
asset/
	banner.png
	backgrounds/
		bg_black.png
		bg_white.png
```

## Can only have one depth of directory

```txt
example/
	*/
```

This structure would be valid.

```txt
example/
	hello/
```

This structure would be invalid.

```txt
example/
	hello/
		not_ok/
```
