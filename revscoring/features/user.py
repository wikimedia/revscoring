import re

from ..datasources import revision_metadata, user_info
from .feature import Feature

USER_REGISTRATION_EPOCH = Timestamp("20050101000000")
"""
Date that registrations started being recorded
"""

def process_is_anon(revision_metadata):
    
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None

is_anon = Feature("user.is_anon", process_is_anon,
                  returns=bool, depends_on=[revision_metadata])


def process_is_bot(user_info):
    
    return "bot" in user_info.groups

is_bot = Feature("user.is_bot", process,
                 returns=bool, depends_on=[user_info])

def process_user_age_in_seconds(user_info, revision_metadata):
    
    if user_info.id is None: # Anonymous
        return 0
    else:
        return revision_metadata.timestamp - \
               (user_info.registration or USER_REGISTRATION_EPOCH)

age_in_seconds = Feature("user.age_in_seconds", process,
                         returns=int,
                         depends_on=[user_info, revision_metadata])
