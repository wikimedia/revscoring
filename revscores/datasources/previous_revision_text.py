from ..util.dependencies import depends
from .previous_rev_doc import previous_rev_doc


@depends(on=[previous_rev_doc])
def previous_revision_text(previous_rev_doc):
    return previous_rev_doc.get("*")
