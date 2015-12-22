import re

from ....feature import Feature
from ....meta import aggregators
from .datasources import Datasources


class ParsedRevision:

    def __init__(self, prefix, text_datasource, parent_text_datasource=None):
        self.datasources = Datasources(prefix, text_datasource)

        self.content_chars = aggregators.len(
            self.datasources.content,
            name=prefix + ".content_chars"
        )
        """
        The number of characters of viewable content (no markup or templates)
        """

        self.headings = aggregators.len(
            self.datasources.headings,
            name=prefix + ".headings"
        )
        """
        The number of headings
        """

        self.external_links = aggregators.len(
            self.datasources.external_links,
            name=prefix + ".external_links"
        )
        """
        The number of external links
        """

        self.wikilinks = aggregators.len(
            self.datasources.wikilinks,
            name=prefix + ".wikilinks"
        )
        """
        The number of wikilinks (internal to other pages in the wiki)
        """

        self.tags = aggregators.len(
            self.datasources.tags,
            name=prefix + ".tags"
        )
        """
        The number of HTML tags
        """

        self.templates = aggregators.len(
            self.datasources.templates,
            name=prefix + ".templates"
        )
        """
        The number of templates
        """

        if parent_text_datasource is not None:
            self.parent = ParsedRevision(
                prefix + ".parent",
                parent_text_datasource
            )
