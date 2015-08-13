import re

WORD_RE = re.compile('^\w*[^\W\d]\w$', re.I | re.U)
