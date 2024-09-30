import uuid

def parse_to_int(num: str) -> int:
     try:
        return int(num)
     except:
         return None
     
def is_serial_number(word, current_sn):
    """
    Check if the word ends with a period and is a valid serial number
    that follows the current serial number sequence.
    """
    if word.endswith("."):
        number_part = parse_to_int(word[:-1])
        if number_part == current_sn + 1:
            return True
    return False

def find_key_in_range(number, doc_index):
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


def is_valid_uuid(uuid_string):
    if uuid_string is None:
        return False
    try:
        val = uuid.UUID(uuid_string, version=4)
        return True
    except ValueError:
        return False