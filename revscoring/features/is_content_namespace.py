from ..datasources import namespaces, revision_metadata
from .feature import Feature


def process(revision_metadata, namespaces):
    
    content_namespace_ids = set(ns.id for ns in namespaces.values() if ns.content)
    
    return revision_metadata.page_namespace in content_namespace_ids

is_content_namespace = Feature("is_content_namespace", process, returns=bool,
                               depends_on=[revision_metadata, namespaces])
