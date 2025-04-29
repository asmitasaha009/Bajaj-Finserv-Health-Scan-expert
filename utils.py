import re

# Regular expressions used to match lab test details
# Test name: match strings that start with letters and may contain digits, spaces, and special characters
TEST_NAME_RE = re.compile(r'^[A-Za-z][A-Za-z0-9 \-()/+,]*')

# Value regex: matches a number, optionally followed by a unit (e.g., "mg/dL", "mmol/L")
VALUE_RE = re.compile(r'([-+]?\d*\.?\d+)\s*([a-zA-Z%µ/]+)?')   # Captures value & unit

# Range regex: matches a range like "70-110", "10 to 20", or "12 / 15"
RANGE_RE = re.compile(
    r'([-+]?\d*\.?\d+)\s*(?:–|-|to|/)\s*([-+]?\d*\.?\d+)',
    flags=re.I
)

def clean(text: str) -> str:
    """Normalize OCR quirks like fancy dashes, multiple spaces, and character misreads."""
    # Replace various dash types with a single standard dash
    text = text.replace('—', '-').replace('–', '-')
    
    # Replace tab characters and multiple spaces with single space
    text = text.replace('\t', ' ').replace('  ', ' ')  # Two spaces for simplicity
    
    # Correct common OCR misreads: O↔0 and l↔1
    text = text.replace('O', '0').replace('l', '1')
    
    # Return the cleaned text with extra spaces collapsed into a single space
    return " ".join(text.split())
