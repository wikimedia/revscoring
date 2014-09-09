from ..util.dependencies import depends
from .rev_doc import rev_doc


@depends(on=[rev_doc])
def revision_text(rev_doc):
    return rev_doc.get("*")
