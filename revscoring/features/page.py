from ..datasources import page_creation, revision, site
from .feature import Feature


def process_is_content_namespace(revision_metadata, namespace_map):
    return namespace_map[revision_metadata.page_namespace].content

is_content_namespace = \
        Feature("page.is_content_namespace", process_is_content_namespace,
                returns=bool,
                depends_on=[revision.metadata, site.namespace_map])

def process_is_mainspace(revision_metadata):
    return revision_metadata.page_namespace == 0

is_mainspace = Feature("page.is_mainspace", process_is_mainspace,
                       returns=bool,
                       depends_on=[revision.metadata])

def process_age(page_creation_metadata, revision_metadata):
    return revision_metadata.timestamp - page_creation_metadata.timestamp

age = Feature("page.age", process_age,
              returns=int,
              depends_on=[page_creation.metadata, revision.metadata])
