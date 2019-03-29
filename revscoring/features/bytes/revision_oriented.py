from revscoring.datasources import revision_oriented
from revscoring.dependencies import DependentSet

from ..meta import aggregators
from . import datasources

name = "bytes.revision"


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.length = aggregators.len(
            revision_datasources.bytes,
            name=name + ".length"
        )
        "`int` : The length of the revision content in bytes"

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )
            """
            :class:`revscoring.features.bytes.Revision` : The
            parent (aka "previous") revision of the page.
            """


revision = Revision(name,
                    datasources.Revision(name, revision_oriented.revision))
"""
Represents the base revision of interest.  Implements this a basic structure:

* revision: :class:`~revscoring.features.bytes.Revision`
    * parent: :class:`~revscoring.features.bytes.Revision`
"""
