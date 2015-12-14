from . import parent_revision, revision
from ..datasource import Datasource
from .util import diff_dicts


def process_sitelinks_diff(past_item, current_item):
    past_sitelinks = past_item.sitelinks if past_item is not None else {}
    return diff_dicts(past_sitelinks, current_item.sitelinks)

sitelinks_diff = Datasource("diff.sitelinks_diff", process_sitelinks_diff,
                            depends_on=[parent_revision.item, revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of sitelinks keys
"""


def process_labels_diff(past_item, current_item):
    past_labels = past_item.labels if past_item is not None else {}
    return diff_dicts(past_labels, current_item.labels)

labels_diff = Datasource("diff.labels_diff", process_labels_diff,
                         depends_on=[parent_revision.item, revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of labels keys
"""


def process_aliases_diff(past_item, current_item):
    past_aliases = past_item.aliases if past_item is not None else {}
    return diff_dicts(past_aliases, current_item.aliases)

aliases_diff = Datasource("diff.aliases_diff", process_aliases_diff,
                          depends_on=[parent_revision.item, revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of alias keys
"""


def process_descriptions_diff(past_item, current_item):
    past_descriptions = past_item.descriptions if past_item is not None else {}
    return diff_dicts(past_descriptions, current_item.descriptions)

descriptions_diff = Datasource("diff.descriptions_diff",
                               process_descriptions_diff,
                               depends_on=[parent_revision.item,
                                           revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of description
keys
"""


def process_claims_diff(past_item, current_item):
    past_claims = past_item.claims if past_item is not None else {}
    return diff_dicts(past_claims, current_item.claims)

claims_diff = Datasource("diff.claims_diff",
                         process_claims_diff,
                         depends_on=[parent_revision.item, revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of description
keys
"""


def process_badges_diff(past_item, current_item):
    past_badges = past_item.badges if past_item is not None else {}
    return diff_dicts(past_badges, current_item.badges)

badges_diff = Datasource("diff.badges_diff",
                         process_badges_diff,
                         depends_on=[parent_revision.item, revision.item])
"""
Generates a :class`~revscoring.datasources.wikibase.DiffDict` of badge
keys
"""


def process_added_claims(claims_diff, past_item, current_item):
    added_claims = []
    for p_number in claims_diff.added:
        added_claims += current_item.claims[p_number]
    for p_number in claims_diff.changed:
        parent_guids = [claim.snak for claim in past_item.claims[p_number]]
        for claim in current_item.claims[p_number]:
            if claim.snak not in parent_guids:
                added_claims.append(claim)

    return added_claims

added_claims = Datasource("diff.added_claims", process_added_claims,
                          depends_on=[claims_diff, parent_revision.item,
                                      revision.item])
"""
Generates a `list` of description added claims.
"""


def process_removed_claims(claims_diff, past_item, current_item):
    removed_claims = []
    for p_number in claims_diff.removed:
        removed_claims += past_item.claims[p_number]
    for p_number in claims_diff.changed:
        current_guids = [claim.snak for claim in past_item.claims[p_number]]
        for claim in past_item.claims[p_number]:
                if claim.snak not in current_guids:
                    removed_claims.append(claim)

    return removed_claims

removed_claims = Datasource("diff.removed_claims", process_removed_claims,
                            depends_on=[claims_diff, parent_revision.item,
                                        revision.item])
"""
Generates a `list` of description removed claims.
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

changed_claims = Datasource("diff.changed_claims", process_changed_claims,
                            depends_on=[claims_diff, parent_revision.item,
                                        revision.item])
"""
Generates a `list` of changed claims.
"""


def process_added_sources(changed_claims):
    added_sources = []
    for old_claim, new_claim in changed_claims:
        parent_guids = []
        for source in old_claim.sources:
            for p_number in source:
                parent_guids += [claim.hash for claim in source[p_number]]
        for source in new_claim.sources:
            for p_number in source:
                for claim in source[p_number]:
                    if claim.hash not in parent_guids:
                        added_sources.append(claim)
    return added_sources

added_sources = Datasource("diff.added_sources", process_added_sources,
                           depends_on=[changed_claims])
"""
Generates a `list` of added sources.
"""


def process_removed_sources(changed_claims):
    removed_sources = []
    for old_claim, new_claim in changed_claims:
        current_guids = []
        for source in new_claim.sources:
            for p_number in source:
                current_guids += [claim.hash for claim in source[p_number]]
        for source in old_claim.sources:
            for p_number in source:
                for claim in source[p_number]:
                    if claim.hash not in current_guids:
                        removed_sources.append(claim)
    return removed_sources

removed_sources = Datasource("diff.removed_sources", process_removed_sources,
                             depends_on=[changed_claims])
"""
Generates a `list` of removed sources.
"""


def process_added_qualifiers(changed_claims):
    added_qualifiers = []
    for old_claim, new_claim in changed_claims:
        parent_guids = []
        for p_number in old_claim.qualifiers:
            parent_guids += [claim.hash
                             for claim in old_claim.qualifiers[p_number]]
        for p_number in new_claim.qualifiers:
            for claim in new_claim.qualifiers[p_number]:
                if claim.hash not in parent_guids:
                    added_qualifiers.append(claim)
    return added_qualifiers

added_qualifiers = Datasource("diff.added_qualifiers",
                              process_added_qualifiers,
                              depends_on=[changed_claims])
"""
Generates a `list` of removed sources.
"""


def process_removed_qualifiers(changed_claims):
    removed_qualifiers = []
    for old_claim, new_claim in changed_claims:
        current_guids = []
        for p_number in new_claim.qualifiers:
            current_guids += [claim.hash
                              for claim in new_claim.qualifiers[p_number]]
        for p_number in old_claim.qualifiers:
            for claim in old_claim.qualifiers[p_number]:
                if claim.hash not in current_guids:
                    removed_qualifiers.append(claim)
    return removed_qualifiers

removed_qualifiers = Datasource("diff.removed_qualifiers",
                                process_removed_qualifiers,
                                depends_on=[changed_claims])
"""
Generates a `list` of removed qualifiers.
"""
