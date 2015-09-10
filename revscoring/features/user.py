from mwtypes import Timestamp

from ..datasources import revision, user
from .feature import Feature

# Date that registrations started being recorded in MediaWiki
USER_REGISTRATION_EPOCH = Timestamp("20050101000000")


def process_age(user_info, revision_metadata):
    if user_info is None:
        return 0
    if process_is_anon(revision_metadata):  # Anonymous so age == zero
        return 0
    else:
        registration_delta = revision_metadata.timestamp - \
            (user_info.registration or USER_REGISTRATION_EPOCH)
        return max(registration_delta, 0)

age = Feature("user.age", process_age,
              returns=int, depends_on=[user.info, revision.metadata])
"""
Represents age of user when the edit was made in seconds.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [user.age]))
        [33260354]
"""


def process_is_anon(revision_metadata):
    return revision_metadata.user_id == 0 or revision_metadata.user_id is None

is_anon = Feature("user.is_anon", process_is_anon,
                  returns=bool, depends_on=[revision.metadata])
"""
Represents whether the user is anonymous or registered.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [user.is_anon]))
        [False]
"""


def process_is_bot(user_info):
    if user_info is None:
        return False
    return "bot" in user_info.groups

is_bot = Feature("user.is_bot", process_is_bot,
                 returns=bool, depends_on=[user.info])
"""
Represents whether the user is bot or not.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130, [user.is_bot]))
        [False]
"""

all = [age, is_anon, is_bot]
