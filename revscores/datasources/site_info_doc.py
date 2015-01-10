from .datasource import Datasource

def process(session):
    
        doc = session.site_info.query(properties={'namespaces'})
        return doc['query']

