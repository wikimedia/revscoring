import re

from ...meta import aggregators


class Revision:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.content_chars = aggregators.len(
            self.datasources.content,
            name=self._name + ".content_chars"
        )
        """
        `int` : The number of characters of viewable content (no markup or
        templates
        """

        self.headings = aggregators.len(
            self.datasources.headings,
            name=self._name + ".headings"
        )
        "`int` : The number of headings"

        self.external_links = aggregators.len(
            self.datasources.external_links,
            name=self._name + ".external_links"
        )
        "`int` : The number of external links"

        self.wikilinks = aggregators.len(
            self.datasources.wikilinks,
            name=self._name + ".wikilinks"
        )
        "`int` : The number of wikilinks (internal to other pages in the wiki)"

        self.tags = aggregators.len(
            self.datasources.tags,
            name=self._name + ".tags"
        )
        "`int` : The number of HTML tags"

        self.ref_tags = aggregators.len(
            self.datasources.tag_names_matching(r"ref"),
            name=self._name + ".ref_tags"
        )
        "`int` : The number of <ref> tags"

        self.templates = aggregators.len(
            self.datasources.templates,
            name=self._name + ".templates"
        )
        "`int` : The number of templates"

    def heading_titles_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Feature` that that generates a count of
        header titles that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        if name is None:
            name = "{0}({1})".format(self._name + ".heading_titles_matching",
                                     regex.pattern)

        return aggregators.len(
            self.datasources.heading_titles_matching(regex),
            name=name
        )

    def headings_by_level(self, level, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a count of
        all headers of a level.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".headings_by_level",
                                     level)
        return aggregators.len(
            self.datasources.headings_by_level(level),
            name=name
        )

    def external_link_urls_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a count of
        external link URLs that match a regular expression
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".external_link_urls_matching",
                           regex.pattern)

        return aggregators.len(
            self.datasources.external_link_urls_matching(regex),
            name=name
        )

    def wikilink_titles_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that that generates a count
        of wikilink titles names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".wikilink_titles_matching",
                           regex.pattern)

        return aggregators.len(
            self.datasources.wikilink_titles_matching(regex),
            name=name
        )

    def tag_names_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a count of
        tag names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".tag_names_matching", regex.pattern)

        return aggregators.len(
            self.datasources.tag_names_matching(regex),
            name=name
        )

    def template_names_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Feature` that generates a count of
        template names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".template_names_matching",
                           regex.pattern)

        return aggregators.len(
            self.datasources.template_names_matching(regex),
            name=name
        )
