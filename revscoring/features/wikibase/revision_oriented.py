from . import datasources, features
from ...datasources import revision_oriented

prefix = "wikibase.revision"

revision = features.Revision(
    prefix,
    datasources.Revision(prefix, revision_oriented.revision)
)
