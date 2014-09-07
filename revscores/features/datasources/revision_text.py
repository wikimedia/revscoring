from ..dependencies import depends_on
from .rev_doc import rev_doc


@depends_on(rev_doc)
def revision_text(rev_doc):
    return rev_doc.get("*")
