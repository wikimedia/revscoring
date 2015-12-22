import json

import pywikibase

from ....datasources import Datasource


class Datasources:

    def __init__(self, prefix, text_datasource):

        self.item_doc = Datasource(
            prefix + ".item_doc", _process_item_doc,
            depends_on=[text_datasource]
        )
        """
        A JSONable `dict` of content for a Wikibase content.
        """

        self.item = Datasource(
            prefix + ".item", _process_item,
            depends_on=[self.item_doc]
        )
        """
        A `~pywikibase.Item` for the Wikibase content
        """

        self.sitelinks = Datasource(
            prefix + ".sitelinks", _process_sitelinks, depends_on=[self.item]
        )
        """
        A `dict` of wiki/sitelink pairs in the revision
        """

        self.labels = Datasource(
            prefix + ".labels", _process_labels, depends_on=[self.item]
        )
        """
        A `dict` of lang/label pairs in the revision
        """

        self.aliases = Datasource(
            prefix + ".aliases", _process_aliases, depends_on=[self.item]
        )
        """
        A `set` of unique aliases in the revision
        """

        self.descriptions = Datasource(
            prefix + ".descriptions", _process_descriptions,
            depends_on=[self.item]
        )
        """
        A `dict` of lang/description pairs in the revision
        """

        self.claims = Datasource(
            prefix + ".claims", _process_claims, depends_on=[self.item]
        )
        """
        A `set` of unique claims in the revision
        """

        self.sources = Datasource(
            prefix + ".sources", _process_sources, depends_on=[self.item]
        )
        """
        A `set` of unique sources in the revision
        """

        self.qualifiers = Datasource(
            prefix + ".qualifiers", _process_qualifiers, depends_on=[self.item]
        )
        """
        A `set` of unique qualifiers in the revision
        """

        self.badges = Datasource(
            prefix + ".badges", _process_badges, depends_on=[self.item]
        )
        """
        A `set` of unique badges in the revision
        """


def _process_item_doc(text):
    return json.loads(text or "")


def _process_item(item_doc):
    item = pywikibase.ItemPage()
    item.get(content=item_doc)
    return item


def _process_claims(item):
    return set(
        (property, _claim_to_str(claim))
        for property in item.claims
        for claim in item.claims[property]
    )


def _process_aliases(item):
    return set(
        (lang, alias)
        for lang in item.aliases
        for alias in item.aliases[lang]
    )


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
    return set(
        (wiki, badge)
        for wiki in item.badges
        for badge in item.badges[wiki]
    )


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
