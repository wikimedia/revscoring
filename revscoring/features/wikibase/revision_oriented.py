from . import datasources, features
from ...datasources import revision_oriented

name = "wikibase.revision"

revision = features.Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
"""
Represents the base revision of interest.  Implements this basic structure:

* revision: :class:`~revscoring.features.wikibase.Revision`
    * parent: :class:`~revscoring.features.wikibase.Revision`
    * diff: :class:`~revscoring.features.wikibase.Diff`
"""
