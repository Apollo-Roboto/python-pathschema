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


```
