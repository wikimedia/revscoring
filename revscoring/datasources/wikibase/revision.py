import json

import pywikibase

from ...datasources import Datasource
from ..revision import text


def process_item_doc(text):
    return json.loads(text)

item_doc = Datasource("revision.item_doc", process_item_doc,
                      depends_on=[text])
"""
Generates a JSONable `dict` from raw content for a Wikibase revision.
"""


def process_item(item_doc):
    item = pywikibase.ItemPage()
    item.get(content=item_doc)
    return item

item = Datasource("revision.item", process_item,
                  depends_on=[item_doc])
"""
Generates a `~pywikibase.Item`.
"""
