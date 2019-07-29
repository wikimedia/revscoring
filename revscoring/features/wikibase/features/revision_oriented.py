from revscoring.dependencies import DependentSet

from ...feature import Feature
from ...meta import aggregators, bools
from .diff import Diff


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.datasources = revision_datasources

        self.sitelinks = aggregators.len(self.datasources.sitelinks)
        "`int` : A count of sitelinks in the revision"
        self.labels = aggregators.len(self.datasources.labels)
        "`int` : A count of labels in the revision"
        self.aliases = aggregators.len(self.datasources.aliases)
        "`int` : A count of aliases in the revision"
        self.descriptions = aggregators.len(self.datasources.descriptions)
        "`int` : A count of descriptions in the revision"
        self.properties = aggregators.len(self.datasources.properties)
        "`int` : A count of properties in the revision"
        self.claims = aggregators.len(self.datasources.claims)
        "`int` : A count of claims in the revision"
        self.sources = aggregators.len(self.datasources.sources)
        "`int` : A count of sources in the revision"
        self.reference_claims = aggregators.len(
                self.datasources.reference_claims)
        "`int` : A count of reference claims in the revision"
        self.qualifiers = aggregators.len(self.datasources.qualifiers)
        "`int` : A count of qualifiers in the revision"
        self.badges = aggregators.len(self.datasources.badges)
        "`int` : A count of badges in the revision"

        if hasattr(self.datasources, "parent"):
            self.parent = Revision(name + ".parent", self.datasources.parent)
            """
            :class:`revscoring.features.wikibase.Revision` : The
            parent (aka "previous") revision of the page.
            """

        if hasattr(self.datasources, "diff"):
            self.diff = Diff(name + ".diff", self.datasources.diff)
            """
            :class:`~revscoring.features.wikibase.Diff` : The
            difference between this revision and the parent revision.
            """

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

        return HasPropertyValue(name, property, value, self.datasources.entity)


class HasPropertyValue(Feature):
    def __init__(self, name, property, value, item_datasource):
        self.property = property
        self.value = value
        super().__init__(name, self._process, returns=bool,
                         depends_on=[item_datasource])

    def _process(self, item):
        statements = item.properties.get(self.property, [])
        return self.value in (str(s.claim.datavalue) for s in statements)
