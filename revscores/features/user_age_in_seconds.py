from mw import Timestamp

from ..datasources import revision_metadata, user_info
from .feature import Feature


def process(user_info, revision_metadata):
    
    return revision_metadata.timestamp - \
           (user_info.registration or Timestamp("20050101000000"))

user_age_in_seconds = Feature("user_age_in_seconds", process,
                              returns=int,
                              depends_on=[user_info, revision_metadata])
