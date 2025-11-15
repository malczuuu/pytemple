import random
import re
import string
import uuid
import time
from typing import List, Optional
from datetime import datetime, date, timedelta

__UUID_PATTERN = r"\${\s*random\.uuid\s*}"
__INT_PATTERN = r"\${\s*random\.int\s*\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)\s*}"
__BOOLEAN_PATTERN = r"\${\s*random\.boolean\s*}"
__DOUBLE_PATTERN = \
    r"\${\s*random\.double\s*\(\s*(-?[0-9]\d*(?:\.\d+)?)\s*,\s*(-?[0-9]\d*(?:\.\d+)?)\s*\)\s*}"
__STRING_PATTERN = r"\${\s*random\.string\s*\(\s*(\d+)\s*\)\s*}"
__CHOICE_PATTERN = r"\${\s*random\.choice\s*\(\s*(.+?)\s*\)\s*}"

__DATE_PATTERN = r"\${\s*random\.date\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*}"
__DATETIME_PATTERN = r"\${\s*random\.datetime\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)\s*}"
__TIMESTAMP_PATTERN = r"\${\s*random\.timestamp\s*}"
__DATE_PAST_PATTERN = r"\${\s*random\.date\.past\s*\(\s*days\s*=\s*(\d+)\s*\)\s*}"
__DATE_FUTURE_PATTERN = r"\${\s*random\.date\.future\s*\(\s*days\s*=\s*(\d+)\s*\)\s*}"


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
    template = __process_date(template)
    template = __process_datetime(template)
    template = __process_timestamp(template)
    template = __process_date_past(template)
    template = __process_date_future(template)
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


def __process_date(template: str) -> str:
    matches = re.findall(__DATE_PATTERN, template)
    while matches:
        start_raw, end_raw = matches[0]
        start_s = __strip_quotes(start_raw.strip())
        end_s = __strip_quotes(end_raw.strip())
        try:
            start_d = __parse_to_date(start_s)
            end_d = __parse_to_date(end_s)
            if start_d > end_d:
                break
            days = (end_d - start_d).days
            offset = random.randint(0, days)
            chosen = start_d + timedelta(days=offset)
            template = re.sub(__DATE_PATTERN, chosen.isoformat(), template, count=1)
        except Exception:
            break
        matches = re.findall(__DATE_PATTERN, template)
    return template


def __process_datetime(template: str) -> str:
    matches = re.findall(__DATETIME_PATTERN, template)
    while matches:
        start_raw, end_raw = matches[0]
        start_s = __strip_quotes(start_raw.strip())
        end_s = __strip_quotes(end_raw.strip())
        try:
            start_dt = __parse_to_datetime(start_s)
            end_dt = __parse_to_datetime(end_s)
            if start_dt > end_dt:
                break
            span = int((end_dt - start_dt).total_seconds())
            offset = random.randint(0, span)
            chosen_dt = start_dt + timedelta(seconds=offset)
            template = re.sub(__DATETIME_PATTERN, chosen_dt.replace(tzinfo=None).isoformat(sep='T', timespec='seconds'), template, count=1)
        except Exception:
            break
        matches = re.findall(__DATETIME_PATTERN, template)
    return template


def __process_timestamp(template: str) -> str:
    matches = re.findall(__TIMESTAMP_PATTERN, template)
    while matches:
        ts = str(int(time.time()))
        template = re.sub(__TIMESTAMP_PATTERN, ts, template, count=1)
        matches = re.findall(__TIMESTAMP_PATTERN, template)
    return template


def __process_date_past(template: str) -> str:
    matches = re.findall(__DATE_PAST_PATTERN, template)
    while matches:
        days = int(matches[0])
        try:
            now = datetime.now().date()
            start = now - timedelta(days=days)
            span = (now - start).days
            offset = random.randint(0, span)
            chosen = start + timedelta(days=offset)
            template = re.sub(__DATE_PAST_PATTERN, chosen.isoformat(), template, count=1)
        except Exception:
            break
        matches = re.findall(__DATE_PAST_PATTERN, template)
    return template


def __process_date_future(template: str) -> str:
    matches = re.findall(__DATE_FUTURE_PATTERN, template)
    while matches:
        days = int(matches[0])
        try:
            now = datetime.now().date()
            end = now + timedelta(days=days)
            span = (end - now).days
            offset = random.randint(0, span)
            chosen = now + timedelta(days=offset)
            template = re.sub(__DATE_FUTURE_PATTERN, chosen.isoformat(), template, count=1)
        except Exception:
            break
        matches = re.findall(__DATE_FUTURE_PATTERN, template)
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


def __strip_quotes(s: str) -> str:
    if (len(s) >= 2) and ((s[0] == "'" and s[-1] == "'") or (s[0] == '"' and s[-1] == '"')):
        return s[1:-1]
    return s


def __parse_to_date(s: str) -> date:
    # try ISO date first
    try:
        return date.fromisoformat(s)
    except Exception:
        pass
    # try ISO datetime and take date part
    try:
        if 'T' in s:
            # handle trailing Z
            s2 = s
            if s2.endswith('Z'):
                s2 = s2[:-1]
            return datetime.fromisoformat(s2).date()
    except Exception:
        pass
    # try integer epoch seconds
    try:
        ts = int(s)
        return datetime.fromtimestamp(ts).date()
    except Exception:
        raise ValueError("Invalid date format")


def __parse_to_datetime(s: str) -> datetime:
    # try ISO datetime first
    try:
        s2 = s
        if s2.endswith('Z'):
            s2 = s2[:-1]
        return datetime.fromisoformat(s2)
    except Exception:
        pass
    # try integer epoch seconds
    try:
        ts = int(s)
        return datetime.fromtimestamp(ts)
    except Exception:
        raise ValueError("Invalid datetime format")
