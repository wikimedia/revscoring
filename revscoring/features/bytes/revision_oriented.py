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
        "`int` : The length of the bytes of the revision content in bytes"

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )
            """
            :class:`revscoring.features.bytes.Revision` : The length of the
            bytes of the revision content in bytes
            """

revision = Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
