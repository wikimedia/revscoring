import re

from ..datasources import revision_metadata
from .feature import Feature


def process(revision_metadata):
    
    return revision_metadata.page_namespace == 0

is_mainspace = Feature("is_mainspace", process, returns=bool,
                       depends_on=[revision_metadata])
