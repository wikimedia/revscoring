import re

import mwparserfromhell

from .....datasources import Datasource
from .....datasources.meta import filters, mappers
from .....errors import RevisionNotFound


class Datasources:

    def __init__(self, prefix, text_datasource):
        self.prefix = prefix

        self.wikicode = Datasource(
            prefix + ".wikicode",
            _process_wikicode, depends_on=[text_datasource]
        )
        """
        A :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax
        tree representing the structure of the page.
        """

        self.content = execute_method(
            "strip_code", self.wikicode,
            name=prefix + ".content"
        )
        """
        The viewable content (no markup or templates) of the revision.
        """

        self.headings = execute_method(
            "filter_headings", self.wikicode,
            name=prefix + ".headings"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Heading`'s
        """

        self.heading_titles = mappers.map(
            _extract_heading_title, self.headings,
            name=prefix + ".heading_titles"
        )
        """
        A list of heading titles
        """

        self.external_links = execute_method(
            "filter_external_links", self.wikicode,
            name=prefix + ".external_links"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.ExternalLink`'s
        """

        self.external_link_urls = mappers.map(
            _extract_external_link_url, self.external_links,
            name=prefix + ".external_link_url"
        )
        """
        A list of external link urls
        """

        self.wikilinks = execute_method(
            "filter_wikilinks", self.wikicode,
            name=prefix + ".wikilinks"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Wikilink`'s
        """

        self.wikilink_titles = mappers.map(
            _extract_wikilink_title, self.wikilinks,
            name=prefix + ".wikilink_titles"
        )
        """
        Returns a list of string titles of internal links (aka "targets")
        """

        self.tags = execute_method(
            "filter_tags", self.wikicode,
            name=prefix + ".tags"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Tag`'s
        """

        self.tag_names = mappers.map(
            _extract_tag_name, self.tags,
            name=prefix + ".tag_names"
        )
        """
        Returns a list of html tag names present in the content of the revision
        """

        self.templates = execute_method(
            "filter_templates", self.wikicode,
            name=prefix + ".templates"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Templates`'s
        """

        self.template_names = mappers.map(
            _extract_template_name, self.templates,
            name=prefix + ".template_names"
        )
        """
        Returns a list of template names present in the content of the revision
        """

    def heading_titles_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list` of
        all header titles that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        if name is None:
            name = "{0}({1})".format(self.prefix + ".heading_titles_matching",
                                     regex.pattern)
        return filters.regex_matching(regex, self.heading_titles, name=name)

    def headings_by_level(self, level, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list` of
        all headers of a level.
        """
        if name is None:
            name = "{0}({1})".format(self.prefix + ".headings_by_level",
                                     level)
        return filters.filter(HeadingOfLevel(level).filter, self.headings,
                              name=name)

    def external_link_urls_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list` of
        external link URLs that match a regular expression
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self.prefix + ".external_link_urls_matching",
                           regex.pattern)

        return filters.regex_matching(regex, self.external_link_urls,
                                      name=name)

    def wikilink_titles_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list`
        of internal link titles names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self.prefix + ".wikilink_titles_matching",
                           regex.pattern)

        return filters.regex_matching(regex, self.wikilink_titles, name=name)

    def tag_names_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all tag names
        that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self.prefix + ".tag_names_matching", regex.pattern)

        return filters.regex_matching(regex, self.tag_names, name=name)

    def template_names_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all template
        names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self.prefix + ".template_names_matching",
                           regex.pattern)

        return filters.regex_matching(regex, self.template_names, name=name)


def _process_wikicode(text):
    return mwparserfromhell.parse(text)


def _extract_heading_title(heading):
    return str(heading.title).strip()


def _extract_external_link_url(elink):
    return str(elink.url)


def _extract_wikilink_title(wikilinks):
    return str(wikilinks.title)


def _extract_tag_name(tag):
    return str(tag.tag)


def _extract_template_name(template):
    return str(template.name)


class HeadingOfLevel:
    def __init__(self, level):
        self.level = int(level)

    def filter(self, heading):
        return heading.level == self.level


class execute_method(Datasource):
    def __init__(self, method_name, object_datasource, args=None, kwargs=None,
                 name=None):
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs
        name = self._format_name(name, [object_datasource])
        super().__init__(name, self.process, depends_on=[object_datasource])

    def process(self, object):
        args = self.args or []
        kwargs = self.kwargs or {}
        return getattr(object, self.method_name)(*args, **kwargs)
