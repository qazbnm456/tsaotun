"""This module provides a workaround function using json.JSONDecoder.raw_decode"""

import re
import json

nonspace = re.compile(r'\S')


def json_iterparse(j):
    """A workaround function using json.JSONDecoder.raw_decode"""
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded
