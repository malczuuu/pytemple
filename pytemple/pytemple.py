import random
import re
import string
import uuid

__UUID_PATTERN = r"\${\s*random\.uuid\s*}"
__INT_PATTERN = r"\${\s*random\.int\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*}"
__BOOLEAN_PATTERN = r"\${\s*random\.boolean\s*}"
__DOUBLE_PATTERN = \
    r"\${\s*random\.double\s*\(\s*(-?[0-9]\d*(?:\.\d+)?)\s*,\s*(-?[0-9]\d*(?:\.\d+)?)\s*\)\s*}"
__STRING_PATTERN = r"\${\s*random\.string\s*\(\s*(\d+)\s*\)\s*}"


def load(filename: str) -> str:
    with open(filename) as file:
        return loads(file.read())


def loads(content: str) -> str:
    return __process(content)


def __process(template: str) -> str:
    template = __process_int(template)
    template = __process_boolean(template)
    template = __process_double(template)
    template = __process_string(template)
    template = __process_uuid(template)
    return template


def __process_int(template: str) -> str:
    matches = re.findall(__INT_PATTERN, template)
    while matches:
        since, until = matches[0]
        template = re.sub(__INT_PATTERN, str(random.randint(int(since), int(until))), template, 1)
        matches = re.findall(__INT_PATTERN, template)
    return template


def __process_boolean(template: str) -> str:
    matches = re.findall(__BOOLEAN_PATTERN, template)
    while matches:
        value = "true" if random.randint(0, 1) == 1 else "false"
        template = re.sub(__BOOLEAN_PATTERN, value, template, 1)
        matches = re.findall(__BOOLEAN_PATTERN, template)
    return template


def __process_double(template: str) -> str:
    matches = re.findall(__DOUBLE_PATTERN, template)
    while matches:
        since, until = matches[0]
        value = str(random.uniform(float(since), float(until)))
        template = re.sub(__DOUBLE_PATTERN, value, template, 1)
        matches = re.findall(__DOUBLE_PATTERN, template)
    return template


def __process_string(template: str) -> str:
    matches = re.findall(__STRING_PATTERN, template)
    while matches:
        size = matches[0]
        template = re.sub(__STRING_PATTERN, __random_string(int(size)), template, 1)
        matches = re.findall(__STRING_PATTERN, template)
    return template


def __process_uuid(template: str) -> str:
    matches = re.findall(__UUID_PATTERN, template)
    while matches:
        template = re.sub(__UUID_PATTERN, str(uuid.uuid4()), template, 1)
        matches = re.findall(__UUID_PATTERN, template)
    return template


def __random_string(length: int = 20) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
