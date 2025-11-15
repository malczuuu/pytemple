# PyTemple

Replacing value placeholders in template files.

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
6. `${random.choice(a, b, ...)}` - replace with a random choice from the provided arguments. Arguments may be
   single-word unquoted, or quoted (`'` or `"`).
7. `${random.date(start, end)}` - replace with a random date (format: `YYYY-MM-DD`) between `start` and `end`. Dates may
   be quoted or unquoted and can be ISO dates or epoch seconds.
8. `${random.datetime(start, end)}` - replace with a random datetime (format: `YYYY-MM-DDTHH:MM:SS`) between `start` and
   `end`. datetimes may be quoted or unquoted and can be ISO datetimes or epoch seconds.
9. `${random.timestamp}`- replace with the current Unix timestamp (seconds since epoch).
10. `${random.date.past(days=N)}` - replace with a random date within the past `N` days (inclusive).
11. `${random.date.future(days=N)}` - replace with a random date within the next `N` days (inclusive).

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
