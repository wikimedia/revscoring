from .datasource import Datasource
from .previous_rev_doc import previous_rev_doc


def process(previous_rev_doc):
    return previous_rev_doc.get("*")

previous_revision_text = Datasource("previous_revision_text", process,
                                    depends_on=[previous_rev_doc])
