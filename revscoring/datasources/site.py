from .datasource import Datasource

namespace_map = Datasource("site.namespace_map")
"""
Returns a `dict` of namespace_id : :class:`mw.types.Namespace` pairs for the
MediaWiki installation.
"""
