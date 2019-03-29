"""
.. autoclass:: revscoring.features.wikibase.Diff
    :members:
    :member-order: bysource
"""
from revscoring.datasources import Datasource
from revscoring.dependencies import DependentSet

from ..util import diff_dicts


class Diff(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.revision_entity = revision_datasources.entity
        self.parent_entity = revision_datasources.parent.entity

        # sitelinks
        self.sitelinks_diff = Datasource(
            name + ".sitelinks_diff", diff_dicts,
            depends_on=[revision_datasources.parent.sitelinks,
                        revision_datasources.sitelinks]
        )
        self.sitelinks_added, self.sitelinks_removed, self.sitelinks_changed =\
            diff_parts(name + ".sitelinks", self.sitelinks_diff)

        # labels
        self.labels_diff = Datasource(
            name + ".labels_diff", diff_dicts,
            depends_on=[revision_datasources.parent.labels,
                        revision_datasources.labels]
        )
        self.labels_added, self.labels_removed, self.labels_changed = \
            diff_parts(name + ".labels", self.labels_diff)

        # aliases
        self.aliases_diff = Datasource(
            name + ".aliases_diff", diff_dicts,
            depends_on=[revision_datasources.parent.aliases,
                        revision_datasources.aliases]
        )
        self.aliases_added, self.aliases_removed, self.aliases_changed = \
            diff_parts(name + ".aliases", self.aliases_diff)

        # descriptions
        self.descriptions_diff = Datasource(
            name + ".descriptions_diff", diff_dicts,
            depends_on=[revision_datasources.parent.descriptions,
                        revision_datasources.descriptions]
        )
        (self.descriptions_added, self.descriptions_removed,
         self.descriptions_changed) = \
            diff_parts(name + ".descriptions", self.descriptions_diff)

        # properties
        self.properties_diff = Datasource(
            name + ".properties_diff", diff_dicts,
            depends_on=[revision_datasources.parent.properties,
                        revision_datasources.properties]
        )
        (self.properties_added, self.properties_removed,
         self.properties_changed) = \
            diff_parts(name + ".properties", self.properties_diff)

        self.statements_added = Datasource(
            name + ".statements_added", _process_statements_added,
            depends_on=[self.properties_diff, self.parent_entity,
                        self.revision_entity]
        )
        self.claims_added = Datasource(  # Backwards compatible
            name + ".claims_added", _identity,
            depends_on=[self.statements_added]
        )
        self.statements_removed = Datasource(
            name + ".statements_removed", _process_statements_removed,
            depends_on=[self.properties_diff, self.parent_entity,
                        self.revision_entity]
        )
        self.claims_removed = Datasource(  # Backwards compatible
            name + ".claims_removed", _identity,
            depends_on=[self.statements_removed]
        )
        self.statements_changed = Datasource(
            name + ".statements_changed", _process_statements_changed,
            depends_on=[self.properties_diff, self.parent_entity,
                        self.revision_entity]
        )
        self.claims_changed = Datasource(  # Backwards compatible
            name + ".claims_changed", _identity,
            depends_on=[self.statements_changed]
        )
        self.sources_added = Datasource(
            name + ".sources_added", _process_sources_added,
            depends_on=[self.claims_changed]
        )
        self.sources_removed = Datasource(
            name + ".sources_removed", _process_sources_removed,
            depends_on=[self.claims_changed]
        )
        self.qualifiers_added = Datasource(
            name + ".qualifiers_added", _process_qualifiers_added,
            depends_on=[self.claims_changed]
        )
        self.qualifiers_removed = Datasource(
            name + ".qualifiers_removed", _process_qualifiers_removed,
            depends_on=[self.claims_changed]
        )

        # badges
        self.badges_diff = Datasource(
            name + ".badges_diff", diff_dicts,
            depends_on=[revision_datasources.parent.badges,
                        revision_datasources.badges]
        )
        self.badges_added, self.badges_removed, self.badges_changed = \
            diff_parts(name + ".badges", self.badges_diff)


def diff_parts(name, diff):
    return (
        dict_diff_field("added", diff, name=name + "_added"),
        dict_diff_field("removed", diff, name=name + "_removed"),
        dict_diff_field("changed", diff, name=name + "_changed")
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
        name = self._format_name(name, [field_name, diff_datasource])
        super().__init__(name, self.process, depends_on=[diff_datasource])

    def process(self, diff):
        return getattr(diff, self.field_name)


def _process_statements_added(properties_diff, past_entity, current_entity):
    statements_added = []
    for pid in properties_diff.added:
        statements_added += current_entity.properties[pid]
    for pid in properties_diff.changed:
        parent_guids = {statement.id for statement in past_entity.properties[pid]}
        for statement in current_entity.properties[pid]:
            if statement.id not in parent_guids:
                statements_added.append(statement)

    return statements_added


def _process_statements_removed(properties_diff, past_entity, current_entity):
    statements_removed = []
    for pid in properties_diff.removed:
        statements_removed += past_entity.properties[pid]
    for pid in properties_diff.changed:
        current_guids = {statement.id
                         for statement in past_entity.properties[pid]}
        for statement in past_entity.properties[pid]:
            if statement.id not in current_guids:
                statements_removed.append(statement)

    return statements_removed


def _process_statements_changed(properties_diff, past_entity, current_entity):
    statements_changed = []
    for property in properties_diff.changed:
        parent_guids = {statement.id: statement
                        for statement in past_entity.properties[property]}
        for new_statement in current_entity.properties[property]:
            if new_statement.id in parent_guids and \
               new_statement not in past_entity.properties[property]:
                old_statement = parent_guids[new_statement.id]
                statements_changed.append((old_statement, new_statement))

    return statements_changed


def _process_sources_added(statements_changed):
    sources_added = []
    for old_statement, new_statement in statements_changed:
        parent_guids = {reference.hash
                        for pid in old_statement.references
                        for reference in old_statement.references[pid]}
        for pid in new_statement.references:
            for reference in new_statement.references[pid]:
                if reference.hash not in parent_guids:
                    sources_added.append(reference)
    return sources_added


def _process_sources_removed(statements_changed):
    sources_removed = []
    for old_statement, new_statement in statements_changed:
        current_guids = {reference.hash
                         for pid in new_statement.references
                         for reference in new_statement.references[pid]}
        for pid in old_statement.references:
            for reference in old_statement.references[pid]:
                if reference.hash not in current_guids:
                    sources_removed.append(reference)
    return sources_removed


def _process_qualifiers_added(statements_changed):
    qualifiers_added = []
    for old_statement, new_statement in statements_changed:
        parent_guids = {qualifier.hash
                        for pid in old_statement.qualifiers
                        for qualifier in old_statement.qualifiers[pid]}
        for pid in old_statement.qualifiers:
            for qualifier in old_statement.qualifiers[pid]:
                if qualifier.hash not in parent_guids:
                    qualifiers_added.append(qualifier)
    return qualifiers_added


def _process_qualifiers_removed(statements_changed):
    qualifiers_removed = []
    for old_statement, new_statement in statements_changed:
        current_guids = {qualifier.hash
                         for pid in new_statement.qualifiers
                         for qualifier in new_statement.qualifiers[pid]}
        for pid in old_statement.qualifiers:
            for qualifier in old_statement.qualifiers[pid]:
                if qualifier.hash not in current_guids:
                    qualifiers_removed.append(qualifier)
    return qualifiers_removed


def _identity(value):
    return value
