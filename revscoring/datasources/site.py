import mw

from .datasource import Datasource


def process_info_doc(session):
    
        doc = session.site_info.query(properties={'general', 'namespaces',
                                                  'namespacealiases'})
        return doc

info_doc = Datasource("site.info_doc", process_info_doc, depends_on=['session'])


def process_namespace_map(site_info_doc):
    
    aliases = site_info_doc.get('namespacealiases', [])
    for alias_doc in aliases:
        prev_list = aliases.get(alias_doc['id'], [])
        prev_list.append(alias_doc['*'])
        aliases[alias_doc['id']] = prev_list
    
    namespace_map = {}
    for ns_doc in site_info_doc.get('namespaces', {}).values():
        namespace = mw.Namespace.from_doc(ns_doc, aliases=aliases)
        namespace_map[namespace.id] = namespace

namespace_map = Datasource("site.namespace_map", process_namespace_map,
                           depends_on=[info_doc])
