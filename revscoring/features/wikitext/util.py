import re

MARKUP_RE = re.compile(r'(\[|\]|\{\||\|\}|\|-|\{\{|\}\})+')
NUMERIC_RE = re.compile(r'\d+')
SYMBOLIC_RE = re.compile(r'[^\w0-9\s\n\r]+')
