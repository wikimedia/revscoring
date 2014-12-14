import re

from ..datasources import revision_text
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('\w+', re.UNICODE)

@depends(on=["language", revision_text])
@returns(int)
def prev_misspellings(language, revision_text):
    
    misspellings = 0
    
    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for misspelling in language.misspellings(words):
        misspellings += 1
        
    return misspellings
