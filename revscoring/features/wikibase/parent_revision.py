import json

import pywikibase

from ...datasources import Datasource
from ..parent_revision import text


# Datsources ##################################################################

def process_item_doc(text):
    if text is None:
        return None
    else:
        doc = json.loads(text)
        return doc

item_doc = Datasource("parent_revision.item_doc", process_item_doc,
                      depends_on=[text])
"""
Generates a JSONable `dict` from raw content for a Wikibase revision.
"""


def process_item(item_doc):
    if item_doc is None:
        return None
    else:
        item = pywikibase.ItemPage()
        item.get(content=item_doc)
        return item

item = Datasource("parent_revision.item", process_item,
                  depends_on=[item_doc])
"""
Generates a `~pywikibase.Item`.
"""


# Features ####################################################################
