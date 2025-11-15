# PyTemple

**Note** that this is a library for development/testing tools, so the performance is not a primary concern.

## Table of Contents

- [Placeholders](#placeholders)
- [Installing](#installing)
- [Usage](#usage)
- [Example](#example)

## Placeholders

This chapter describes all supported placeholders that can be used in template files.

1. `${random.uuid}` - replace with a random UUID value.
2. `${random.int(min, max)}` - replace with a random integer within the specified range.
3. `${random.double(min, max)}` - replace with a random double (floating-point number) within the specified range.
4. `${random.boolean}` - replace with a random boolean value (`true` or `false`).
5. `${random.string(size)}` - replace with a random string of the given size.

## Installing

* Using [Poetry](https://python-poetry.org/):
   ```bash
   $ poetry add git+https://github.com/malczuuu/pytemple.git#1.1.0
   ```
* Using [Pipenv](https://github.com/pypa/pipenv):
   ```bash
  $ pipenv install git+https://github.com/malczuuu/pytemple@1.1.0#egg=pytemple
  ```

## Usage

```python
import pytemple

with open("template.txt") as file:
    template = file.read()

template = pytemple.loads(template)
```

## Example

Following template

```txt
{
  "uuid": "${random.uuid}",
  "double": ${random.double(-10, 10)},
  "integer": ${random.int(20, 30)},
  "boolean": ${random.boolean},
  "string": "${random.string(10)}"
}
```

would be translated as

```txt
{
  "uuid": "00772bf8-8f21-4f73-8ca0-30a5354cf935",
  "double": -3.006947539966321,
  "integer": 17,
  "boolean": true,
  "string": "cdtllavjhl"
}
```
