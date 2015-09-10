from mwtypes import Timestamp

from ..datasources import previous_user_revision, revision
from .feature import Feature


def process_seconds_since(pur_metadata, revision_metadata):
    revision_timestamp = \
        revision_metadata.timestamp \
        if revision_metadata is not None and \
        revision_metadata.timestamp is not None \
        else Timestamp(0)
    previous_timestamp = \
        pur_metadata.timestamp \
        if pur_metadata is not None and \
        pur_metadata.timestamp is not None \
        else revision_timestamp

    return revision_timestamp - previous_timestamp

seconds_since = Feature("previous_user_revision", process_seconds_since,
                        returns=int,
                        depends_on=[previous_user_revision.metadata,
                                    revision.metadata])
"""
Represents seconds between last edit and the edit before that.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import revision
        >>> list(extractor.extract(655097130,
        ...      [previous_user_revision.seconds_since]))
        [438]
"""

all = [seconds_since]
