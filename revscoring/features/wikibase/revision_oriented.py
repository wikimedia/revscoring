from . import datasources, features
from ...datasources import revision_oriented

name = "wikibase.revision"

revision = features.Revision(
    name,
    datasources.Revision(name, revision_oriented.revision)
)
