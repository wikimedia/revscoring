from .datasource import datasource_processor
from .previous_rev_doc import previous_rev_doc


@datasource_processor([previous_rev_doc])
def previous_revision_text(previous_rev_doc):
    return previous_rev_doc.get("*")
