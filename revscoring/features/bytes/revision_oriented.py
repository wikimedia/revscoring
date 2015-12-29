from . import datasources
from ...datasources import revision_oriented
from ...dependencies import DependentSet
from ..meta import aggregators

name = "bytes.revision"


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.length = aggregators.len(
            revision_datasources.bytes,
            name=name + ".length"
        )

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )

revision = Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
