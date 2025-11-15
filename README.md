# PyTemple

Replacing value placeholders in template files. 

| Placeholder key               | Description                                                                                                             |
|-------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `${random.uuid}`              | Replace with random UUID value.                                                                                         |
| `${random.int(min, max)}`     | Replace with random integer within range.                                                                               |
| `${random.double(min, max)}`  | Replace with random double within range.                                                                                |
| `${random.boolean}`           | Replace with random boolean.                                                                                            |
| `${random.string(size)}`      | Replace with random string with size.                                                                                   |
| `${random.choice(a, b, ...)}` | Replace with a random choice from provided arguments (arguments may be single-word unquoted or quoted with `'` or `"`). |

## Installing

* Using [Pipenv](https://github.com/pypa/pipenv):

   ```bash
  $ pipenv install git+https://github.com/malczuuu/pytemple@1.0.0#egg=pytemple
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
