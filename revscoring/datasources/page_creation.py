from .datasource import Datasource

metadata = Datasource("page_creation.metadata")
"""
Returns a :class:`~revscoring.datasources.types.RevisionMetadata` for the
revision that created the page.
"""
