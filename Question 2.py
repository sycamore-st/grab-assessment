import re
import pandas as pd

"""
Assumption: I assume all addresses, except for landed addresses, have indicated their floor numbers.
"""


# Make up address user input:
addresses = [
    # correct format (block number, unit number, postal code)
    '101 Marlow Street, #12-05 Clife Parkview, Singapore 059020',

    # correct format, but with a space before and after the hyphen in the unit number or floor number
    '101 Marlow Street, #12 - 05 Clife Parkview, Singapore 059020',

    # missing leading zero for the unit number or floor num, which should be #12-05 to standardize the format
    '#12-5 Clife Parkview, Singapore 059020',
    '#2-5 Clife Parkview, Singapore 059020',

    # basement floor unit number (B1 represents the basement level, which is valid in many buildings with underground
    # units)
    '#B1-5 Clife Parkview, Singapore 059020',

    # landed property, no unit or floor number (common for landed homes like terrace houses or bungalows)
    'No. 29 Hougang St 99 Singapore 111111',

    # address with "Floor" and "Unit" written separately (rather than in #XX-YY format)
    'Block 123 Toa Payoh Lorong 1, Floor 12, Unit 345, Singapore 310123',
    'Block 123, Floor 02, Unit 345, Singapore 310123',
    'Block 123, floor2, Unit 345, Singapore 310123',
    'Block 123, floor b2, Unit 345, Singapore 310123'
]

input_data = pd.DataFrame({'Address': addresses})


def extract_floor(address):
    # Check for the format like #12-05, #12 - 05, or #BX-XX (basement unit)
    match_unit = re.search(
        r'#([B\d]{1,2})\s*-\s*\d+',
        address
    )
    if match_unit:
        return match_unit.group(1).upper()  # Returns the floor part (e.g., '12', 'B1')

    # Check for format like 'Floor XX' or 'FloorXX' (explicit floor number format)
    match_floor = re.search(r'floor\s*([A-Za-z]?\d+)', address, re.IGNORECASE)
    if match_floor:
        return match_floor.group(1).upper()  # Returns the floor number (e.g., '12', 'B2)

    # If no floor found, return None (could be landed properties or no floor mentioned)
    return None


def format_floor_number(
        floor_str: str
):
    if floor_str:
        # If the floor number has only one digit, add a leading zero
        if len(floor_str) == 1:
            return f'0{floor_str}'

    return floor_str


output_data = input_data.copy()
output_data['Floor'] = output_data['address'].apply(extract_floor)

print(output_data)
