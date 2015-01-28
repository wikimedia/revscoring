from .datasource import Datasource


def process(session):
    
        doc = session.site_info.query(properties={'namespaces'})
        return doc

site_info_doc = Datasource("site_info_doc", process, depends_on=['session'])
