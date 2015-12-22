from . import datasources
from ...feature import Feature
from ...meta import aggregators

# Sitelinks
sitelinks_added = aggregators.len(datasources.sitelinks_added)
sitelinks_removed = aggregators.len(datasources.sitelinks_removed)
sitelinks_changed = aggregators.len(datasources.sitelinks_changed)

# Labels
labels_added = aggregators.len(datasources.labels_added)
labels_removed = aggregators.len(datasources.labels_removed)
labels_changed = aggregators.len(datasources.labels_changed)

# Aliases
aliases_added = aggregators.len(datasources.aliases_added)
aliases_removed = aggregators.len(datasources.aliases_removed)
aliases_changed = aggregators.len(datasources.aliases_changed)

# Descriptions
descriptions_added = aggregators.len(datasources.descriptions_added)
descriptions_removed = aggregators.len(datasources.descriptions_removed)
descriptions_changed = aggregators.len(datasources.descriptions_changed)

# Claims
claims_added = aggregators.len(datasources.claims_added)
claims_removed = aggregators.len(datasources.claims_removed)
claims_changed = aggregators.len(datasources.claims_changed)

# Sources
sources_added = aggregators.len(datasources.sources_added)
sources_removed = aggregators.len(datasources.sources_removed)

# Qualifiers
qualifiers_added = aggregators.len(datasources.qualifiers_added)
qualifiers_removed = aggregators.len(datasources.qualifiers_removed)

# Badges
badges_added = aggregators.len(datasources.badges_added)
badges_removed = aggregators.len(datasources.badges_removed)
badges_changed = aggregators.len(datasources.badges_changed)


class property_changed(Feature):
    """
    Returns True if a property has changed.

    :Parameters:
        property : `str`
            The property name
        name : `str`
            A name to associate with the feature.  If not set, the feature's
            name will be 'wikibase.diff.property_changed(<property>)'
    """
    def __init__(self, property, name=None):
        self.property = property
        if name is None:
            name = "wikibase.diff.property_changed({0})".format(repr(property))

        super().__init__(name, self.process, returns=bool,
                         depends_on=[datasources.claims_changed])

    def process(self, claims_changed):
        return self.property in [claims[0].id for claims in claims_changed]
