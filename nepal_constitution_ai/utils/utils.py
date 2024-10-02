import uuid
from typing import Union

def parse_to_int(num: str) -> Union[int, None]:
     try:
        return int(num)
     except:
         return None
     
def is_serial_number(word: str, current_sn: int) -> bool:
    """
    Check if the word ends with a period and is a valid serial number
    that follows the current serial number sequence.
    """
    if word.endswith("."):
        number_part = parse_to_int(word[:-1])
        if number_part == current_sn + 1:
            return True
    return False

def find_key_in_range(number: int, doc_index: dict) -> Union[str, None]:
    """
    Find the corresponding key in the doc_index for a given number.
    
    Args:
    number (int): The number to find in the index range.
    doc_index (dict): A dictionary where the values are ranges in the format 'start-end'.
    
    Returns:
    str: The key corresponding to the range that contains the number, or None if not found.
    """
    for key, value in doc_index.items():
        try:
            start, end = map(int, value.split('-'))
            if start <= number <= end:
                return key
        except ValueError:
            continue  # Skip if value cannot be parsed into a range
    return None


def is_valid_uuid(uuid_string: str) -> bool:
    if uuid_string is None:
        return False
    try:
        uuid.UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False