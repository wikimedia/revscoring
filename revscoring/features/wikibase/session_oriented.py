from revscoring.datasources import session_oriented
from revscoring.dependencies import DependentSet

from . import datasources, features

name = "wikibase.session"


class Session(DependentSet):
    """
    Represents an editor's activity session
    """
    def __init__(self, name, revisions_datasources):
        super().__init__(name)
        session_revision = features.Revision(
            name + ".revisions",
            datasources.Revision(name, revisions_datasources))
        self.revisions = session_oriented.list_of_tree(
            session_revision, rewrite_name=session_oriented.rewrite_name,
            cache={d.name: d for d in revisions_datasources})
        """
        :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.wikibase.Revision`) :
        The revisions saved by the users within the session.
        """

session = Session(name, session_oriented.session.revisions)
"""
Represents an editor's activity session.  Implements this basic structure:
* session: :class:`~revscoring.features.wikibase.Session`
    * revisions: a :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.wikibase.Revision`)
        * parent: a :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.wikibase.Revision`)
        * diff: a a :class:`~revscoring.datasources.meta.expanders.list_of`(:class:`~revscoring.features.wikibase.Diff`)
"""
