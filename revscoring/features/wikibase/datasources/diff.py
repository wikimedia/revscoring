from ....datasources import Datasource
from ..util import diff_dicts


class Diff:

    def __init__(self, prefix, revision_datasources):
        self.prefix = prefix

        self.revision_item = revision_datasources.item
        self.parent_item = revision_datasources.parent.item

        # sitelinks
        self.sitelinks_diff = Datasource(
            prefix + ".sitelinks_diff", diff_dicts,
            depends_on=[revision_datasources.parent.sitelinks,
                        revision_datasources.sitelinks]
        )
        self.sitelinks_added, self.sitelinks_removed, self.sitelinks_changed =\
            diff_parts(prefix + ".sitelinks", self.sitelinks_diff)

        # labels
        self.labels_diff = Datasource(
            prefix + ".labels_diff", diff_dicts,
            depends_on=[revision_datasources.parent.labels,
                        revision_datasources.labels]
        )
        self.labels_added, self.labels_removed, self.labels_changed = \
            diff_parts(prefix + ".labels", self.labels_diff)

        # aliases
        self.aliases_diff = Datasource(
            prefix + ".aliases_diff", diff_dicts,
            depends_on=[revision_datasources.parent.aliases,
                        revision_datasources.aliases]
        )
        self.aliases_added, self.aliases_removed, self.aliases_changed = \
            diff_parts(prefix + ".aliases", self.aliases_diff)

        # descriptions
        self.descriptions_diff = Datasource(
            prefix + ".descriptions_diff", diff_dicts,
            depends_on=[revision_datasources.parent.descriptions,
                        revision_datasources.descriptions]
        )
        (self.descriptions_added, self.descriptions_removed,
         self.descriptions_changed) = \
                diff_parts(prefix + ".descriptions", self.descriptions_diff)

        # properties
        self.properties_diff = Datasource(
            prefix + ".properties_diff", diff_dicts,
            depends_on=[revision_datasources.parent.properties,
                        revision_datasources.properties]
        )
        (self.properties_added, self.properties_removed,
         self.properties_changed) = \
            diff_parts(prefix + ".properties", self.properties_diff)

        self.claims_added = Datasource(
            prefix + ".claims_added", _process_claims_added,
            depends_on=[self.properties_diff, self.parent_item,
                        self.revision_item]
        )
        self.claims_removed = Datasource(
            prefix + ".claims_removed", _process_claims_removed,
            depends_on=[self.properties_diff, self.parent_item,
                        self.revision_item]
        )
        self.claims_changed = Datasource(
            prefix + ".claims_changed", _process_claims_changed,
            depends_on=[self.properties_diff, self.parent_item,
                        self.revision_item]
        )
        self.sources_added = Datasource(
            prefix + ".sources_added", _process_sources_added,
            depends_on=[self.claims_changed]
        )
        self.sources_removed = Datasource(
            prefix + ".sources_removed", _process_sources_removed,
            depends_on=[self.claims_changed]
        )
        self.qualifiers_added = Datasource(
            prefix + ".qualifiers_added", _process_qualifiers_added,
            depends_on=[self.claims_changed]
        )
        self.qualifiers_removed = Datasource(
            prefix + ".qualifiers_removed", _process_qualifiers_removed,
            depends_on=[self.claims_changed]
        )

        # badges
        self.badges_diff = Datasource(
            prefix + ".badges_diff", diff_dicts,
            depends_on=[revision_datasources.parent.badges,
                        revision_datasources.badges]
        )
        self.badges_added, self.badges_removed, self.badges_changed = \
            diff_parts(prefix + ".badges", self.badges_diff)


def diff_parts(prefix, diff):
    return (
        dict_diff_field("added", diff, name=prefix + "_added"),
        dict_diff_field("removed", diff, name=prefix + "_removed"),
        dict_diff_field("changed", diff, name=prefix + "_changed")
    )


class dict_diff_field(Datasource):
    """
    Returns a key set for a dict diff.

    :Parameters:
        field_name : `str`
            The property name to extract
        diff : :class:`~revscoring.features.wikibase.DictDiff`
            A name to associate with the Datasource.  If not set, the feature's
            name will be 'wikibase.diff.dict_diff_field(<property>)'
    """
    def __init__(self, field_name, diff_datasource, name=None):
        self.field_name = field_name
        if name is None:
            name = "dict_diff_field({0})".format(repr(field_name))
        super().__init__(name, self.process, depends_on=[diff_datasource])

    def process(self, diff):
        return getattr(diff, self.field_name)


def _process_claims_added(properties_diff, past_item, current_item):
    claims_added = []
    for property in properties_diff.added:
        claims_added += current_item.claims[property]
    for property in properties_diff.changed:
        parent_guids = {claim.snak for claim in past_item.claims[property]}
        for claim in current_item.claims[property]:
            if claim.snak not in parent_guids:
                claims_added.append(claim)

    return claims_added


def _process_claims_removed(properties_diff, past_item, current_item):
    claims_removed = []
    for property in properties_diff.removed:
        claims_removed += past_item.claims[property]
    for property in properties_diff.changed:
        current_guids = {claim.snak
                         for claim in past_item.claims[property]}
        for claim in past_item.claims[property]:
                if claim.snak not in current_guids:
                    claims_removed.append(claim)

    return claims_removed


def _process_claims_changed(properties_diff, past_item, current_item):
    claims_changed = []
    for property in properties_diff.changed:
        parent_guids = {claim.snak:claim
                        for claim in past_item.claims[property]}
        for claim in current_item.claims[property]:
            if claim.snak in parent_guids and \
               claim not in past_item.claims[property]:
                claims_changed.append((parent_guids[claim.snak], claim))

    return claims_changed


def _process_sources_added(claims_changed):
    sources_added = []
    for old_claim, new_claim in claims_changed:
        parent_guids = []
        for source in old_claim.sources:
            for property in source:
                parent_guids += {claim.hash for claim in source[property]}
        for source in new_claim.sources:
            for property in source:
                for claim in source[property]:
                    if claim.hash not in parent_guids:
                        sources_added.append(claim)
    return sources_added

    sources_added = Datasource(prefix + ".sources_added",
                               process_sources_added,
                               depends_on=[claims_changed])


def _process_sources_removed(claims_changed):
    sources_removed = []
    for old_claim, new_claim in claims_changed:
        current_guids = []
        for source in new_claim.sources:
            for property in source:
                current_guids += {claim.hash for claim in source[property]}
        for source in old_claim.sources:
            for property in source:
                for claim in source[property]:
                    if claim.hash not in current_guids:
                        sources_removed.append(claim)
    return sources_removed


def _process_qualifiers_added(claims_changed):
    qualifiers_added = []
    for old_claim, new_claim in claims_changed:
        parent_guids = []
        for property in old_claim.qualifiers:
            parent_guids += {claim.hash
                             for claim in old_claim.qualifiers[property]}
        for property in new_claim.qualifiers:
            for claim in new_claim.qualifiers[property]:
                if claim.hash not in parent_guids:
                    qualifiers_added.append(claim)
    return qualifiers_added


def _process_qualifiers_removed(claims_changed):
    qualifiers_removed = []
    for old_claim, new_claim in claims_changed:
        current_guids = []
        for property in new_claim.qualifiers:
            current_guids += {claim.hash
                              for claim in new_claim.qualifiers[property]}
        for property in old_claim.qualifiers:
            for claim in old_claim.qualifiers[property]:
                if claim.hash not in current_guids:
                    qualifiers_removed.append(claim)
    return qualifiers_removed
