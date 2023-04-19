# File System Schema

# How to use

```python
import fss

schema = "root/"

path_to_validate = './path'

try:
	fss.validate(path_to_validate, schema)
	print('Valid :)')
except:
	print('Invalid :(')
```

# Example Schema Definition

|  Symbol | Description  | Implemented |
|:-------:|--------------|:-----------:|
| `/` | Slashes at the end of the name marks this element as a folder | X | 
| `*` | Allows files with any name | X |
| `*/` | Allows folder with any name | X |
| `"regex"` | Quotes adds regex validation to the file name | X |
| `"regex"/` | Quotes with a slash adds regex validation to the folder name | X |
| `...` | Allows any (and nested) files and folder | X |
| `[]` | Control the quantity of matching folders/files |   |

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

## Any files and folder allowed in the `assets` folder
```txt
assets/
	...
```

**`-> assets/**/*`**

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

## The `textures` folder can only have files that ends with`.png` or `.gif`.

```txt
assets/
	textures/
		**/
			*.png
			*.gif
	...
```

**`-> assets/textures/**/*.png`**

**`-> assets/textures/**/*.gif`**

This structure would be valid.
```txt
textures/
	robot.png
	skybox.png
	flames.gif
```

This structure would be invalid. *(not ending with .png or .gif)*
```txt
textures/
	robot.fbx
```

## Can only have one depth of directory

```txt
example/
	*/
```

**`-> assets/*/`**

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
