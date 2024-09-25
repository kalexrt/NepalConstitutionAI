from loguru import logger
from nepal_constitution_ai.data_pipeline.loader import load_pdf
from nepal_constitution_ai.utils.utils import parse_to_int, find_key_in_range, is_serial_number
import re

# List of range of articles corresponding to the toc Parts in the constitution
toc_articles_index = ["1-9", "10-15", "16-48", "49-55", "56-60", "61-73", "74-82", "83-108", "109-114", "115-125", "126-156", "157-161", "162-174", "175-196", "197-202", "203-213", "214-220", "221-227", "228-230", "231-237", "238-239", "240-241", "242-244", "245-247", "248-249", "250-251", "252-265", "266-268", "269-272", "273-273", "274-274", "275-294", "295-305", "306-306", "307-308"]


def format_content(pages: str ) -> str:
    formatted_content = ""
    for page in pages:
        formatted_content += page.page_content
    return formatted_content

def format_pdf_section(file_path: str) -> dict:
    content = load_pdf(file_path)
    toc = content[1:5] # Page content from page 2 to page 5
    preamble = content[5:7] # Page content from page 6 to page 7
    articles = content[7:220] # Page content from page 8 to page 220
    schedules = content[220:] # Page content from page 221 to the end
    
    return {
        "toc": format_content(toc),
        "preamble": format_content(preamble),
        "articles": format_content(articles),
        "schedules": format_content(schedules)
    }

def chunk_content_by_section(content: str) -> list[str]:
    """
    Split the given content into sections based on serial numbers.
    Each section starts after a serial number (e.g., 1., 2., 3., etc.).
    """
    sn_count = 0
    section = ""
    chunked_data = []

    for word in content.split():
        # Check if the word is a serial number and increase sn_count
        if is_serial_number(word, sn_count):
            if section.strip():  # Add previous section if it's not empty
                chunked_data.append(section.strip())
            section = ""  # Reset section for new content
            sn_count += 1

        # Start accumulating words for the next section after serial number is found
        if sn_count > 0:
            section += " " + word

    # Append the last section
    if section.strip():
        chunked_data.append(section.strip())

    return chunked_data

def is_schedule_marker(prev_word: str, current_word: str, current_sn: int) -> bool:
    """
    Check if the previous word is 'Schedule' and the current word starts 
    with a number that matches the next expected serial number.
    """
    if prev_word == "Schedule":
        try:
            # Extract the number after the first character in current_word and compare it
            schedule_number = parse_to_int(current_word[1:])
            if schedule_number == current_sn + 1:
                return True
        except (IndexError, ValueError):
            return False
    return False

def chunk_schedule_content(content: str) -> list[str]:
    """
    Chunk content by sections starting with 'Schedule' followed by a serial number.
    """
    words = content.split()
    sn_count = 0
    section = ""
    chunked_data = []

    for i, word in enumerate(words):
        if i > 0 and is_schedule_marker(words[i-1], word, sn_count):
            if section.strip():  # Add previous section if it's not empty
                chunked_data.append(section.strip())
            section = "Schedule"  # Start a new section with 'Schedule'
            sn_count += 1

        if sn_count > 0:
            section += " " + word

    # Append the last section
    if section.strip():
        chunked_data.append(section.strip())

    return chunked_data

def is_letter_marker(word: str, current_letter: int) -> bool:
    """
    Check if the word starts with a letter pattern, e.g., (a), (b), (c), 
    and matches the expected next letter in sequence.
    """
    if len(word) == 3 and word[0] == "(" and word[2] == ")" and ord(word[1]) == current_letter + 1:
        return True
    return False

def split_by_letter_marker(content: str, start_letter="a") -> list[str]:
    """
    Split the given content into sections based on letter markers such as (a), (b), (c), etc.
    """
    letter = ord(start_letter) - 1  # Initialize letter counter
    section = ""
    initial_text = ""
    sections = []

    for word in content.split():
        if is_letter_marker(word, letter):
            letter += 1  # Move to the next letter
            if section.strip():  # Append the previous section if it's not empty
                sections.append(section.strip())
            if not initial_text:  # Store the first section as initial_text
                initial_text = section.strip()
            section = ""  # Reset for the new section
        
        section += " " + word

    # Append the last section
    if section.strip():
        sections.append(section.strip())

    return sections


def parse_table_of_contents(toc_content: str, toc_index: dict) -> dict:
    """
    Parse the table of contents (TOC) from a formatted string, linking section headers to details.

    Args:
    toc_content (str): The formatted TOC string, with sections separated by newlines.
    toc_index (list): A list of indexes to associate with the sections.

    Returns:
    dict: A dictionary where keys are section headers and values are associated details.
    """
    toc = {}
    toc_lines = toc_content.split("\n")
    sn_count = 0

    for i, line in enumerate(toc_lines):
        line = line.strip()

        # Find numeric entries in the line (e.g., section numbers)
        section_number = re.findall(r'\b\d+\b', line)

        # Check if the line contains both text and a section number
        if section_number and len(line) > len(section_number[0]):
            # Ensure there's a next non-empty line for the value
            next_line = toc_lines[i+1].strip() if i+1 < len(toc_lines) else ""
            next_line_2 = toc_lines[i+2].strip() if i+2 < len(toc_lines) else ""

            # Use the next valid line as the value
            value = next_line if next_line else next_line_2
            toc[line] = value
            sn_count += 1

    # Build the document index
    doc_index = {}
    for i, (section, detail) in enumerate(toc.items()):
        if i < len(toc_index):
            doc_index[f"{section.strip()}:{detail.strip()}"] = toc_index[i]
        else:
            doc_index[f"{section.strip()}:{detail.strip()}"] = section

    return doc_index


def populate_chunked_data_dict(articles: list,schedules: list, doc_index: dict) -> list[dict]:
    """
    Populate a list of dictionaries with metadata and text chunks.
    
    Args:
    chunked_data (list): The list of text chunks to be processed.
    doc_index (dict): The document index containing metadata ranges.
    
    Returns:
    list: A list of dictionaries where each dictionary maps metadata to a chunk of text.
    """
    chunked_data_dict_list = []

    # Process the first 51 chunks with keys found by find_key_in_range
    for i, chunk in enumerate(articles[:51]):
        metadata = find_key_in_range(i + 1, doc_index)
        chunked_data_dict_list.append({metadata: chunk})

    # Process chunks 51 to 63 with a fixed metadata key
    for chunk in articles[51:64]:
        metadata = find_key_in_range(51, doc_index)
        chunked_data_dict_list.append({metadata: chunk})

    # Process chunks 64 to 320, skipping empty or whitespace-only chunks
    for i, chunk in enumerate(articles[64:]):
        if chunk.strip():  # Ensure the chunk has meaningful content
            metadata = find_key_in_range(i + 52, doc_index)
            chunked_data_dict_list.append({metadata: chunk})

    # Process the first 9 chunks of schedules with a fixed metadata key
    for i, chunk in enumerate(schedules):
        if chunk.strip():
            # Adjust index to reference correct key from doc_index
            metadata = list(doc_index.keys())[(i - 9)]
            chunked_data_dict_list.append({metadata: chunk})

    return chunked_data_dict_list


def chunk_pdf_content(file_path: str) ->  list:
    """main function to chunk the pdf content"""

    pdf_sections = format_pdf_section(file_path)
    logger.info("Chunking PDF content...")
    articles = chunk_content_by_section(pdf_sections["articles"])
    schedules = chunk_schedule_content(pdf_sections["schedules"])
    article51_sub_articles = split_by_letter_marker(articles[50])
    articles.pop(50)
    for i in range(len(article51_sub_articles)):
        articles.insert(i+50, article51_sub_articles[i])

    doc_index = parse_table_of_contents(pdf_sections["toc"], toc_articles_index)
    chunked_data_dict_list = populate_chunked_data_dict(articles, schedules, doc_index)

    chunked_data_dict_list.insert(0, {"preamble": pdf_sections["preamble"]})

    chunked_data = [pdf_sections["preamble"]] + articles + schedules
    logger.info("Chunking PDF content completed.")
    return chunked_data_dict_list, chunked_data