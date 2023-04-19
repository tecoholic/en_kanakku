from typing import List


def find_comma_indexes(string: str) -> List[int]:
    """Find the indexes of all the commas in the given string"""
    comma_indexes = []
    for index, char in enumerate(string):
        if char == ",":
            comma_indexes.append(index)
    return comma_indexes


def split_string(string: str, end_markers: List[int]) -> List[str]:
    """Splits the given string into multiple substrings using the list of end markers."""
    start = 0
    substrings = []
    for end in end_markers:
        substrings.append(string[start:end])
        start = end
    substrings.append(string[start:])
    return substrings
