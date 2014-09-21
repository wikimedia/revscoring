import re

from ..datasources import revision_text
from ..util.dependencies import depends
from ..util.returns import returns

WORD_RE = re.compile('[a-zA-Z]+', re.UNICODE)

@depends(on=["language", revision_text])
@returns(int)
def prev_badwords(language, revision_text):
    
    badwords = 0
    
    words = (m.group(0) for m in WORD_RE.finditer(revision_text))
    for badword in language.badwords(words):
        badwords += 1
        
    return badwords
