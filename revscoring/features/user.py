import re

from mw import Timestamp

from ..datasources import revision, user
from .feature import Feature

USER_REGISTRATION_EPOCH = Timestamp("20050101000000")
"""
Date that registrations started being recorded in MediaWiki
"""

def process_age(user_info, revision_metadata):

    if process_is_anon(revision_metadata): # Anonymous so age == zero
        return 0
    else:
        return revision_metadata.timestamp - \
               (user_info.registration or USER_REGISTRATION_EPOCH)

age = Feature("user.age", process_age,
              returns=int, depends_on=[user.info, revision.metadata])


def process_is_anon(revision_metadata):

    return revision_metadata.user_id == 0 or revision_metadata.user_id is None

is_anon = Feature("user.is_anon", process_is_anon,
                  returns=bool, depends_on=[revision.metadata])


def process_is_bot(user_info):

    return "bot" in user_info.groups

is_bot = Feature("user.is_bot", process_is_bot,
                 returns=bool, depends_on=[user.info])

all = [age, is_anon, is_bot]
