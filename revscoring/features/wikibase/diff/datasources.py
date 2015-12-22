from ....datasources import Datasource
from ..revision_oriented import revision
from ..util import diff_dicts

prefix = "wikibase.diff"
revision_item = revision.datasources.item
parent_item = revision.parent.datasources.item


def process_sitelinks_diff(past_item, current_item):
    past_sitelinks = past_item.sitelinks if past_item is not None else {}
    return diff_dicts(past_sitelinks, current_item.sitelinks)

sitelinks_diff = Datasource(prefix + ".sitelinks_diff", process_sitelinks_diff,
                            depends_on=[parent_item, revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of sitelinks keys
"""


def process_labels_diff(past_item, current_item):
    past_labels = past_item.labels if past_item is not None else {}
    return diff_dicts(past_labels, current_item.labels)

labels_diff = Datasource(prefix + ".labels_diff", process_labels_diff,
                         depends_on=[parent_item, revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of labels keys
"""


def process_aliases_diff(past_item, current_item):
    past_aliases = past_item.aliases if past_item is not None else {}
    return diff_dicts(past_aliases, current_item.aliases)

aliases_diff = Datasource(prefix + ".aliases_diff", process_aliases_diff,
                          depends_on=[parent_item, revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of alias keys
"""


def process_descriptions_diff(past_item, current_item):
    past_descriptions = past_item.descriptions if past_item is not None else {}
    return diff_dicts(past_descriptions, current_item.descriptions)

descriptions_diff = Datasource(prefix + ".descriptions_diff",
                               process_descriptions_diff,
                               depends_on=[parent_item,
                                           revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of description
keys
"""


def process_claims_diff(past_item, current_item):
    past_claims = past_item.claims if past_item is not None else {}
    return diff_dicts(past_claims, current_item.claims)

claims_diff = Datasource(prefix + ".claims_diff",
                         process_claims_diff,
                         depends_on=[parent_item, revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of description
keys
"""


def process_badges_diff(past_item, current_item):
    past_badges = past_item.badges if past_item is not None else {}
    return diff_dicts(past_badges, current_item.badges)

badges_diff = Datasource(prefix + ".badges_diff",
                         process_badges_diff,
                         depends_on=[parent_item, revision_item])
"""
A :class`~revscoring.datasources.wikibase.DiffDict` of badge
keys
"""


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
            name = prefix + ".dict_diff_field({0})"\
                   .format(repr(field_name))

        super().__init__(name, self.process, depends_on=[diff_datasource])

    def process(self, diff):
        return getattr(diff, self.field_name)


# sitelinks
sitelinks_added = dict_diff_field(
    "added", sitelinks_diff,
    name=prefix + ".sitelinks_added"
)
"""
A `set` of sitelinks that were added in the edit
"""

sitelinks_removed = dict_diff_field(
    "removed", sitelinks_diff,
    name=prefix + ".sitelinks_removed"
)
"""
A `set` of sitelinks that were removed in the edit
"""

sitelinks_changed = dict_diff_field(
    "changed", sitelinks_diff,
    name=prefix + ".sitelinks_changed"
)
"""
A `set` of sitelinks that were changed in the edit
"""

# labels
labels_added = dict_diff_field(
    "added", labels_diff,
    name=prefix + ".labels_added"
)
"""
A `set` of labels that were added in the edit
"""

labels_removed = dict_diff_field(
    "removed", labels_diff,
    name=prefix + ".labels_removed"
)
"""
A `set` of labels that were removed in the edit
"""

labels_changed = dict_diff_field(
    "changed", labels_diff,
    name=prefix + ".labels_changed"
)
"""
A `set` of labels that were changed in the edit
"""

# aliases
aliases_added = dict_diff_field(
    "added", aliases_diff,
    name=prefix + ".aliases_added"
)
"""
A `set` of aliases that were added in the edit
"""

aliases_removed = dict_diff_field(
    "removed", aliases_diff,
    name=prefix + ".aliases_removed"
)
"""
A `set` of aliases that were removed in the edit
"""

aliases_changed = dict_diff_field(
    "changed", aliases_diff,
    name=prefix + ".aliases_changed"
)
"""
A `set` of aliases that were changed in the edit
"""

# descriptions
descriptions_added = dict_diff_field(
    "added", descriptions_diff,
    name=prefix + ".descriptions_added"
)
"""
A `set` of descriptions that were added in the edit
"""

descriptions_removed = dict_diff_field(
    "removed", descriptions_diff,
    name=prefix + ".descriptions_removed"
)
"""
A `set` of descriptions that were removed in the edit
"""

descriptions_changed = dict_diff_field(
    "changed", descriptions_diff,
    name=prefix + ".descriptions_changed"
)
"""
A `set` of descriptions that were changed in the edit
"""

# claims
claims_added = dict_diff_field(
    "added", claims_diff,
    name=prefix + ".claims_added"
)
"""
A `set` of claims that were added in the edit
"""

claims_removed = dict_diff_field(
    "removed", claims_diff,
    name=prefix + ".claims_removed"
)
"""
A `set` of claims that were removed in the edit
"""

claims_changed = dict_diff_field(
    "changed", claims_diff,
    name=prefix + ".claims_changed"
)
"""
A `set` of claims that were changed in the edit
"""

# badges
badges_added = dict_diff_field(
    "added", badges_diff,
    name=prefix + ".badges_added"
)
"""
A `set` of badges that were added in the edit
"""

badges_removed = dict_diff_field(
    "removed", badges_diff,
    name=prefix + ".badges_removed"
)
"""
A `set` of badges that were removed in the edit
"""

badges_changed = dict_diff_field(
    "changed", badges_diff,
    name=prefix + ".badges_changed"
)
"""
A `set` of badges that were removed in the edit
"""


def process_claims_added(claims_diff, past_item, current_item):
    claims_added = []
    for p_number in claims_diff.added:
        claims_added += current_item.claims[p_number]
    for p_number in claims_diff.changed:
        parent_guids = [claim.snak for claim in past_item.claims[p_number]]
        for claim in current_item.claims[p_number]:
            if claim.snak not in parent_guids:
                claims_added.append(claim)

    return claims_added

claims_added = Datasource(prefix + ".claims_added", process_claims_added,
                          depends_on=[claims_diff, parent_item,
                                      revision_item])
"""
A `list` of added claims.
"""


def process_claims_removed(claims_diff, past_item, current_item):
    claims_removed = []
    for p_number in claims_diff.removed:
        claims_removed += past_item.claims[p_number]
    for p_number in claims_diff.changed:
        current_guids = [claim.snak for claim in past_item.claims[p_number]]
        for claim in past_item.claims[p_number]:
                if claim.snak not in current_guids:
                    claims_removed.append(claim)

    return claims_removed

claims_removed = Datasource(prefix + ".claims_removed", process_claims_removed,
                            depends_on=[claims_diff, parent_item,
                                        revision_item])
"""
A `list` of removed claims.
"""


def process_changed_claims(claims_diff, past_item, current_item):
    changed_claims = []
    for p_number in claims_diff.changed():
        parent_guids = {claim.snak:claim
                        for claim in past_item.claims[p_number]}
        for claim in current_item.claims[p_number]:
            if claim.snak in parent_guids and \
               claim not in past_item.claims[p_number]:
                changed_claims.append(tuple([parent_guids[claim.snak], claim]))

    return changed_claims

changed_claims = Datasource(prefix + ".changed_claims", process_changed_claims,
                            depends_on=[claims_diff, parent_item,
                                        revision_item])
"""
A `list` of changed claims.
"""


def process_sources_added(changed_claims):
    sources_added = []
    for old_claim, new_claim in changed_claims:
        parent_guids = []
        for source in old_claim.sources:
            for p_number in source:
                parent_guids += [claim.hash for claim in source[p_number]]
        for source in new_claim.sources:
            for p_number in source:
                for claim in source[p_number]:
                    if claim.hash not in parent_guids:
                        sources_added.append(claim)
    return sources_added

sources_added = Datasource(prefix + ".sources_added",
                           process_sources_added,
                           depends_on=[changed_claims])
"""
A `list` of added sources.
"""


def process_sources_removed(changed_claims):
    sources_removed = []
    for old_claim, new_claim in changed_claims:
        current_guids = []
        for source in new_claim.sources:
            for p_number in source:
                current_guids += [claim.hash for claim in source[p_number]]
        for source in old_claim.sources:
            for p_number in source:
                for claim in source[p_number]:
                    if claim.hash not in current_guids:
                        sources_removed.append(claim)
    return sources_removed

sources_removed = Datasource(prefix + ".sources_removed", process_sources_removed,
                             depends_on=[changed_claims])
"""
A `list` of removed sources.
"""


def process_qualifiers_added(changed_claims):
    qualifiers_added = []
    for old_claim, new_claim in changed_claims:
        parent_guids = []
        for p_number in old_claim.qualifiers:
            parent_guids += [claim.hash
                             for claim in old_claim.qualifiers[p_number]]
        for p_number in new_claim.qualifiers:
            for claim in new_claim.qualifiers[p_number]:
                if claim.hash not in parent_guids:
                    qualifiers_added.append(claim)
    return qualifiers_added

qualifiers_added = Datasource(prefix + ".qualifiers_added",
                              process_qualifiers_added,
                              depends_on=[changed_claims])
"""
A `list` of removed sources.
"""


def process_qualifiers_removed(changed_claims):
    qualifiers_removed = []
    for old_claim, new_claim in changed_claims:
        current_guids = []
        for p_number in new_claim.qualifiers:
            current_guids += [claim.hash
                              for claim in new_claim.qualifiers[p_number]]
        for p_number in old_claim.qualifiers:
            for claim in old_claim.qualifiers[p_number]:
                if claim.hash not in current_guids:
                    qualifiers_removed.append(claim)
    return qualifiers_removed

qualifiers_removed = Datasource(prefix + ".qualifiers_removed",
                                process_qualifiers_removed,
                                depends_on=[changed_claims])
"""
A `list` of removed qualifiers.
"""
