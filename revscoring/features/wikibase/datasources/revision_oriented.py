import json

import mwbase

from revscoring.datasources import Datasource
from revscoring.dependencies import DependentSet
from revscoring.errors import UnexpectedContentType

from .diff import Diff


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.entity_doc = Datasource(
            name + ".entity_doc", _process_entity_doc,
            depends_on=[revision_datasources.text]
        )
        """
        A JSONable `dict` of content for a Wikibase content.
        """

        self.entity = Datasource(
            name + ".entity", _process_entity,
            depends_on=[self.entity_doc]
        )
        """
        A `~mwbase.Entity` for the Wikibase content
        """

        self.sitelinks = Datasource(
            name + ".sitelinks", _process_sitelinks, depends_on=[self.entity]
        )
        """
        A `dict` of wiki/sitelink pairs in the revision
        """

        self.labels = Datasource(
            name + ".labels", _process_labels, depends_on=[self.entity]
        )
        """
        A `dict` of lang/label pairs in the revision
        """

        self.aliases = Datasource(
            name + ".aliases", _process_aliases, depends_on=[self.entity]
        )
        """
        A `set` of unique aliases in the revision
        """

        self.descriptions = Datasource(
            name + ".descriptions", _process_descriptions,
            depends_on=[self.entity]
        )
        """
        A `dict` of lang/description pairs in the revision
        """

        self.properties = Datasource(
            name + ".properties", _process_properties, depends_on=[self.entity]
        )
        """
        A `set` of properties in the revision
        """

        self.claims = Datasource(
            name + ".claim", _process_claims, depends_on=[self.entity]
        )
        """
        A `set` of unique claims in the revision
        """

        self.sources = Datasource(
            name + ".sources", _process_sources, depends_on=[self.entity]
        )
        """
        A `set` of unique sources in the revision
        """

        self.reference_claims = Datasource(
            name + ".reference_claims", _process_ref_claims,
            depends_on=[self.entity]
        )
        """
        A `set` of unique reference claims in the revision
        """

        self.qualifiers = Datasource(
            name + ".qualifiers", _process_qualifiers, depends_on=[self.entity]
        )
        """
        A `set` of unique qualifiers in the revision
        """

        self.badges = Datasource(
            name + ".badges", _process_badges, depends_on=[self.entity]
        )
        """
        A `set` of unique badges in the revision
        """

        if hasattr(revision_datasources, "parent") and \
           hasattr(revision_datasources.parent, "text"):
            self.parent = Revision(
                name + ".parent",
                revision_datasources.parent
            )

            if hasattr(revision_datasources, "diff"):
                self.diff = Diff(name + ".diff", self)


def _process_entity_doc(text):
    if text is not None:
        try:
            return json.loads(text)
        except json.decoder.JSONDecodeError:
            raise UnexpectedContentType(text, "JSON")
    else:
        return None


def _process_entity(text):
    if text is not None:
        return mwbase.Entity.from_json(text)
    else:
        return mwbase.Entity.from_json({})


def _process_properties(entity):
    return entity.properties


def _process_claims(entity):
    return set(
        (pid, str(statement.claim.datavalue))
        for pid, statements in entity.properties.items()
        for statement in statements
    )


def _process_aliases(entity):
    return entity.aliases


def _process_sources(entity):
    """Get reference statements in entity. Returns set."""
    return set(
        (pid, str(statement.claim.datavalue), ref_pid, str(ref[0].datavalue))
        for pid, statements in entity.properties.items()
        for statement in statements
        for ref_pid, ref in statement.references.items()
    )


def _process_ref_claims(entity):
    """Get reference claims in entity. Returns set."""
    return set(
        (pid, str(statement.claim.datavalue), ref_pid, i,
            str(ref_claim.datavalue))
        for pid, statements in entity.properties.items()
        for statement in statements
        for ref_pid, ref_claims in statement.references.items()
        for i, ref_claim in enumerate(ref_claims)
    )


def _process_qualifiers(entity):
    return set(
        (pid, str(statement.claim.datavalue), qualifier_pid, i,
         str(qualifier_claim.datavalue))
        for pid, statements in entity.properties.items()
        for statement in statements
        for qualifier_pid, qualifier_claims in statement.qualifiers.items()
        for i, qualifier_claim in enumerate(qualifier_claims)
    )


def _process_badges(entity):
    return {dbname: sitelink.badges
            for dbname, sitelink in entity.sitelinks.items()
            if len(sitelink.badges) > 0}


def _process_labels(entity):
    return entity.labels


def _process_sitelinks(entity):
    return {dbname: sitelink.title
            for dbname, sitelink in entity.sitelinks.items()}


def _process_descriptions(entity):
    return entity.descriptions
