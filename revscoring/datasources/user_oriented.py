"""
Implements a set of datasources oriented off of a single user.  This is
useful for extracting features of a user, or their first edit.

.. autodata:: revscoring.datasources.revision_oriented.revision

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.datasources.revision_oriented.Revision
    :members:
    :member-order: bysource

.. autoclass:: revscoring.datasources.revision_oriented.Diff
    :members:
    :member-order: bysource

"""
from ..dependencies import DependentSet
from .datasource import Datasource


class User(DependentSet):
    """
    Repersents user-oriented user.
    """
    def __init__(self, name):
        super().__init__(name)
        self.sessions = self.create_sessions(revisions)
        self.first_session = self.sessions[0]
