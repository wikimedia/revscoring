import re

from ..datasources import revision_metadata
from .feature import Feature


def process(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None

user_is_anon = Feature("user_is_anon", process,
                       returns=bool, depends_on=[revision_metadata])
