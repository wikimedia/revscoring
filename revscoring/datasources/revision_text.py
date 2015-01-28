from .datasource import Datasource
from .rev_doc import rev_doc


def process(rev_doc):
    return rev_doc.get("*")

revision_text = Datasource("revision_text", process, depends_on=[rev_doc])
