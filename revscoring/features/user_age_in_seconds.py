from mw import Timestamp

from ..datasources import revision_metadata, user_info
from .feature import Feature

USER_REGISTRATION_EPOCH = Timestamp("20050101000000")
"""
Date that registrations started being recorded
"""

def process(user_info, revision_metadata):
    
    if user_info.id is None: # Anonymous
        return 0
    else:
        return revision_metadata.timestamp - \
               (user_info.registration or USER_REGISTRATION_EPOCH)

user_age_in_seconds = Feature("user_age_in_seconds", process,
                              returns=int,
                              depends_on=[user_info, revision_metadata])
