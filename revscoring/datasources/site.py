import mw

from .datasource import Datasource


def process_doc(session):

        doc = session.site_info.query(properties={'general', 'namespaces',
                                                  'namespacealiases'})
        return doc

doc = Datasource("site.doc", process_doc, depends_on=['session'])


def process_namespace_map(site_info_doc):

    aliases = site_info_doc.get('namespacealiases', [])
    alias_map = {}
    for alias_doc in aliases:
        prev_list = alias_map.get(alias_doc['id'], [])
        prev_list.append(alias_doc['*'])
        alias_map[alias_doc['id']] = prev_list

    namespace_map = {}
    for ns_doc in site_info_doc.get('namespaces', {}).values():
        namespace = mw.Namespace.from_doc(ns_doc, aliases=alias_map)
        namespace_map[namespace.id] = namespace

    return namespace_map

namespace_map = Datasource("site.namespace_map", process_namespace_map,
                           depends_on=[doc])
