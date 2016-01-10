import json

import pywikibase

from ....datasources import Datasource
from ....dependencies import DependentSet
from .diff import Diff


class Revision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)

        self.item_doc = Datasource(
            name + ".item_doc", _process_item_doc,
            depends_on=[revision_datasources.text]
        )
        """
        A JSONable `dict` of content for a Wikibase content.
        """

        self.item = Datasource(
            name + ".item", _process_item,
            depends_on=[self.item_doc]
        )
        """
        A `~pywikibase.Item` for the Wikibase content
        """

        self.sitelinks = Datasource(
            name + ".sitelinks", _process_sitelinks, depends_on=[self.item]
        )
        """
        A `dict` of wiki/sitelink pairs in the revision
        """

        self.labels = Datasource(
            name + ".labels", _process_labels, depends_on=[self.item]
        )
        """
        A `dict` of lang/label pairs in the revision
        """

        self.aliases = Datasource(
            name + ".aliases", _process_aliases, depends_on=[self.item]
        )
        """
        A `set` of unique aliases in the revision
        """

        self.descriptions = Datasource(
            name + ".descriptions", _process_descriptions,
            depends_on=[self.item]
        )
        """
        A `dict` of lang/description pairs in the revision
        """

        self.properties = Datasource(
            name + ".properties", _process_properties, depends_on=[self.item]
        )
        """
        A `set` of properties in the revision
        """

        self.claims = Datasource(
            name + ".claim", _process_claims, depends_on=[self.item]
        )
        """
        A `set` of unique claims in the revision
        """

        self.sources = Datasource(
            name + ".sources", _process_sources, depends_on=[self.item]
        )
        """
        A `set` of unique sources in the revision
        """

        self.qualifiers = Datasource(
            name + ".qualifiers", _process_qualifiers, depends_on=[self.item]
        )
        """
        A `set` of unique qualifiers in the revision
        """

        self.badges = Datasource(
            name + ".badges", _process_badges, depends_on=[self.item]
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


def _process_item_doc(text):
    if text is not None:
        return json.loads(text)
    else:
        return None


def _process_item(item_doc):
    item = pywikibase.ItemPage()
    item.get(content=item_doc or {'aliases': {}})
    return item


def _process_properties(item):
    return item.claims


def _process_claims(item):
    return set(
        (property, _claim_to_str(claim))
        for property in item.claims
        for claim in item.claims[property]
    )


def _process_aliases(item):
    return item.aliases


def _process_sources(item):
    return set(
        (property, _claim_to_str(claim), i)
        for property in item.claims
        for claim in item.claims[property]
        for i, source in enumerate(claim.sources)
    )


def _process_qualifiers(item):
    return set(
        (property, _claim_to_str(claim), qualifier)
        for property in item.claims
        for claim in item.claims[property]
        for qualifier in claim.qualifiers
    )


def _process_badges(item):
    return item.badges


def _process_labels(item):
    return item.labels


def _process_sitelinks(item):
    return item.sitelinks


def _process_descriptions(item):
    return item.descriptions


def _claim_to_str(claim):
    if isinstance(claim.target, pywikibase.ItemPage):
        return str(claim.target.id)
    elif isinstance(claim.target, pywikibase.WbTime):
        return claim.target.toTimestr()
    elif isinstance(claim.target, pywikibase.WbQuantity):
        return repr(claim.target)
    else:
        return str(claim.target)
