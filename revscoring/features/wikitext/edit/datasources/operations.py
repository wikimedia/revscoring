import logging
import time

from deltas import segment_matcher

from .....datasources import Datasource
from ...tokens import revision
from ..util import prefix

logger = logging.getLogger(__name__)


def process_operations(a, b):
    start = time.time()
    operations = [op for op in segment_matcher.diff(a, b)]
    logger.debug("diff() of {0} and {1} tokens took {2} seconds."
                 .format(len(a), len(b), time.time() - start))

    return operations, a, b

operations = Datasource(
    prefix + ".operations", process_operations,
    depends_on=[revision.parent.datasources.tokens,
                revision.datasources.tokens]
)
"""
Returns a tuple that describes the difference between the parent revision text
and the current revision's text.

The tuple contains three fields:

* operations: `list` of :class:`deltas.Operation`
* A tokens: `list` of `str`
* B tokens: `list` of `str`
"""
