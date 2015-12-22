
from ...feature import Feature
from ...meta import aggregators
from .datasources import Datasources


class ParsedRevision:

    def __init__(self, prefix, text_datasource, parent_text_datasource=None):
        self.prefix = prefix

        self.datasources = Datasources(prefix, text_datasource)

        self.sitelinks = aggregators.len(self.datasources.sitelinks)
        self.labels = aggregators.len(self.datasources.labels)
        self.aliases = aggregators.len(self.datasources.aliases)
        self.descriptions = aggregators.len(self.datasources.descriptions)
        self.claims = aggregators.len(self.datasources.claims)
        self.sources = aggregators.len(self.datasources.sources)
        self.qualifiers = aggregators.len(self.datasources.qualifiers)
        self.badges = aggregators.len(self.datasources.badges)

        if parent_text_datasource is not None:
            self.parent = ParsedRevision(
                prefix + ".parent",
                parent_text_datasource
            )

    def has_property(self, property, name=None):
        """
        Returns True if the specified property exists

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            name : `str`
                A name to associate with the feature.  If not set, the feature's
                name will be 'has_property(<property>)'
        """
        if name is None:
            name = self.prefix + ".has_property({0})".format(repr(property))

        return HasProperty(name, property, self.datasources.item)

    def has_property_value(self, property, value, name=None):
        """
        Returns True if the specified property matches the provided value.

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            value : `mixed`
                The value to match
            name : `str`
                A name to associate with the Feature.
        """
        if name is None:
            name = self.prefix + ".has_property_value({0}, {1})" \
                                 .format(repr(property), repr(value))

        return HasPropertyValue(name, property, value, self.datasources.item)


class HasProperty(Feature):
    def __init__(self, name, property, item_datasource):
        self.property = property
        super().__init__(name, self._process, returns=bool,
                         depends_on=[item_datasource])

    def _process(self, item):
        return self.property in item.claims


class HasPropertyValue(Feature):
    def __init__(self, name, property, value, item_datasource):
        self.property = property
        self.value = value
        super().__init__(name, self._process, returns=bool,
                         depends_on=[item_datasource])

    def _process(self, item):
        values = item.claims.get(self.property, [])
        return self.value in (i.target for i in values)
