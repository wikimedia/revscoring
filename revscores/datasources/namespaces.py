from .datasource import Datasource

def process(site_info_doc):
    
    namespaces = {}
    for ns_id, ns_doc in site_info_doc['namespaces'].items():
        ns_id = int(ns_id)
        namespaces[ns_id] = mw.Namespace.from_doc(ns_doc)
        
    return namespaces
