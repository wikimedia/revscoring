import re

CATEGORY_RE = re.compile(r"^category:", re.U | re.I)
CITE_RE = re.compile(r"cite", re.I | re.U)
IMAGE_RE = re.compile(r"^(file|image):", re.U | re.I)
INFOBOX_RE = re.compile(r"infobox|sidebar", re.U | re.I)
MARKUP_RE = re.compile(r'(\[|\]|\{\||\|\}|\|-|\{\{|\}\})+')
NUMERIC_RE = re.compile(r'\d+', re.U)
SECTION_COMMENT_RE = re.compile(r"\/\*([^\*]|\*[^\/])+\*\/")
SYMBOLIC_RE = re.compile(r'[^\w0-9\s\n\r]+', re.U)
# UPPERCASE_RE = re.compile(r'[A-Z]+', re.UNICODE)
