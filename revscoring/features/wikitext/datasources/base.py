from revscoring.dependencies import DependentSet
from . import revision_oriented


class BaseRevision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.text = revision_datasources.text

        if hasattr(revision_datasources, "parent"):
            self.parent = revision_oriented.Revision(
                name + ".parent",
                revision_datasources.parent
            )


class BaseDiff(DependentSet):

    def __init__(self, name, revision):
        super().__init__(name)
        self.revision = revision
