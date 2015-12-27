
from ....dependencies import DependentSet
from ...feature import Feature
from ...meta import aggregators, bools
from .diff import Diff


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.datasources = revision_datasources

        self.sitelinks = aggregators.len(self.datasources.sitelinks)
        self.labels = aggregators.len(self.datasources.labels)
        self.aliases = aggregators.len(self.datasources.aliases)
        self.descriptions = aggregators.len(self.datasources.descriptions)
        self.properties = aggregators.len(self.datasources.properties)
        self.claims = aggregators.len(self.datasources.claims)
        self.sources = aggregators.len(self.datasources.sources)
        self.qualifiers = aggregators.len(self.datasources.qualifiers)
        self.badges = aggregators.len(self.datasources.badges)

        if hasattr(self.datasources, "parent"):
            self.parent = Revision(name + ".parent", self.datasources.parent)

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(name + ".diff", self.datasources.diff)

    def has_property(self, property, name=None):
        """
        Returns True if the specified property exists

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            name : `str`
                A name to associate with the feature.  If not set, the
                feature's name will be 'has_property(<property>)'
        """
        if name is None:
            name = self._name + ".has_property({0})".format(repr(property))

        return bools.item_in_set(property, self.datasources.properties,
                                 name=name)

    def has_property_value(self, property, value, name=None):
        """
        Returns True if the specified property matches the provided value.

        :Parameters:
            property : `str`
                The name of a property (usually preceeded by "P")
            value : `mixed`
                The value to match
            name : `str`
                A name to associate with the Feature. If not set, the
                feature's name will be
                'has_property_value(<property>, <value>)'
        """
        if name is None:
            name = self._name + ".has_property_value({0}, {1})" \
                                 .format(repr(property), repr(value))

        return HasPropertyValue(name, property, value, self.datasources.item)


class HasPropertyValue(Feature):
    def __init__(self, name, property, value, item_datasource):
        self.property = property
        self.value = value
        super().__init__(name, self._process, returns=bool,
                         depends_on=[item_datasource])

    def _process(self, item):
        values = item.claims.get(self.property, [])
        return self.value in (i.target for i in values)
