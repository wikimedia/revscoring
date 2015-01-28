from ..datasources import previous_revision_metadata, revision_metadata
from .feature import Feature


def process(previous_revision_metadata, revision_metadata):
    
    return revision_metadata.timestamp - \
           (previous_revision_metadata.timestamp or
            revision_metadata.timestamp)

seconds_since_last_page_edit = Feature("seconds_since_last_page_edit", process,
                                       returns=int,
                                       depends_on=[previous_revision_metadata,
                                                   revision_metadata])
