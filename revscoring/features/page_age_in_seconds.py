from ..datasources import first_revision_metadata, revision_metadata
from .feature import Feature


def process(first_revision_metadata, revision_metadata):
    
    return revision_metadata.timestamp - first_revision_metadata.timestamp

page_age_in_seconds = Feature("page_age_in_seconds", process,
                              returns=int,
                              depends_on=[first_revision_metadata,
                                          revision_metadata])
