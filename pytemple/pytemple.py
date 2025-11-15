import random
import re
import string
import uuid
from typing import List, Optional

__UUID_PATTERN = r"\${\s*random\.uuid\s*}"
__INT_PATTERN = r"\${\s*random\.int\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*}"
__BOOLEAN_PATTERN = r"\${\s*random\.boolean\s*}"
__DOUBLE_PATTERN = \
    r"\${\s*random\.double\s*\(\s*(-?[0-9]\d*(?:\.\d+)?)\s*,\s*(-?[0-9]\d*(?:\.\d+)?)\s*\)\s*}"
__STRING_PATTERN = r"\${\s*random\.string\s*\(\s*(\d+)\s*\)\s*}"
__CHOICE_PATTERN = r"\${\s*random\.choice\s*\(\s*(.+?)\s*\)\s*}"


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
    template = __process_choice(template)
    template = __process_uuid(template)
    return template


def __process_int(template: str) -> str:
    matches = re.findall(__INT_PATTERN, template)
    while matches:
        since, until = matches[0]
        template = re.sub(__INT_PATTERN, str(random.randint(int(since), int(until))), template, count=1)
        matches = re.findall(__INT_PATTERN, template)
    return template


def __process_boolean(template: str) -> str:
    matches = re.findall(__BOOLEAN_PATTERN, template)
    while matches:
        value = "true" if random.randint(0, 1) == 1 else "false"
        template = re.sub(__BOOLEAN_PATTERN, value, template, count=1)
        matches = re.findall(__BOOLEAN_PATTERN, template)
    return template


def __process_double(template: str) -> str:
    matches = re.findall(__DOUBLE_PATTERN, template)
    while matches:
        since, until = matches[0]
        value = str(random.uniform(float(since), float(until)))
        template = re.sub(__DOUBLE_PATTERN, value, template, count=1)
        matches = re.findall(__DOUBLE_PATTERN, template)
    return template


def __process_string(template: str) -> str:
    matches = re.findall(__STRING_PATTERN, template)
    while matches:
        size = matches[0]
        template = re.sub(__STRING_PATTERN, __random_string(int(size)), template, count=1)
        matches = re.findall(__STRING_PATTERN, template)
    return template


def __process_choice(template: str) -> str:
    matches = re.findall(__CHOICE_PATTERN, template)
    while matches:
        args_str = matches[0]
        args = __split_choice_args(args_str)
        if not args:
            break
        value = random.choice(args)
        template = re.sub(__CHOICE_PATTERN, value, template, count=1)
        matches = re.findall(__CHOICE_PATTERN, template)
    return template


def __process_uuid(template: str) -> str:
    matches = re.findall(__UUID_PATTERN, template)
    while matches:
        template = re.sub(__UUID_PATTERN, str(uuid.uuid4()), template, count=1)
        matches = re.findall(__UUID_PATTERN, template)
    return template


def __random_string(length: int = 20) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def __split_choice_args(s: str) -> Optional[List[str]]:
    """
    Helper to split choice arguments while respecting single and double quotes
    """
    args = []
    cur = ""
    in_single = False
    in_double = False
    i = 0
    while i < len(s):
        c = s[i]
        if c == "'" and not in_double:
            in_single = not in_single
            cur += c
        elif c == '"' and not in_single:
            in_double = not in_double
            cur += c
        elif c == "," and not in_single and not in_double:
            token = cur.strip()
            if token == "":
                return None
            # strip surrounding quotes
            if (token[0] == "'" and token[-1] == "'") or (token[0] == '"' and token[-1] == '"'):
                token = token[1:-1]
            else:
                # unquoted tokens must be single-word (no whitespace)
                if any(ch.isspace() for ch in token):
                    return None
            args.append(token)
            cur = ""
        else:
            cur += c
        i += 1

    if in_single or in_double:
        return None

    token = cur.strip()
    if token == "":
        return None

    if (token[0] == "'" and token[-1] == "'") or (token[0] == '"' and token[-1] == '"'):
        token = token[1:-1]
    else:
        if any(ch.isspace() for ch in token):
            return None

    args.append(token)
    return args
