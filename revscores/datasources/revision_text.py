from .datasource import datasource_processor
from .rev_doc import rev_doc


@datasource_processor([rev_doc])
def revision_text(rev_doc):
    return rev_doc.get("*")
