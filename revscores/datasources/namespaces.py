import mw

from .datasource import Datasource
from .site_info_doc import site_info_doc


def process(site_info_doc):
    
    aliases = {}
    for alias_doc in aliases:
        prev_list = aliases.get(alias_doc['id'], [])
        prev_list.append(alias_doc['*'])
        aliases[alias_doc['id']] = prev_list
    
    namespaces = {}
    for ns_id, ns_doc in site_info_doc['namespaces'].items():
        ns_id = int(ns_id)
        namespaces[ns_id] = mw.Namespace.from_doc(ns_doc, aliases=aliases)
        
    return namespaces

namespaces = Datasource("namespaces", process, depends_on=[site_info_doc])
