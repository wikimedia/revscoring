import re

import mwparserfromhell

from revscoring.datasources import Datasource
from revscoring.datasources.meta import filters, mappers


class Revision:

    def __init__(self, name, revision_datasources):
        super().__init__(name, revision_datasources)

        self.wikicode = Datasource(
            self._name + ".wikicode",
            _process_wikicode, depends_on=[revision_datasources.text]
        )
        """
        A :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax
        tree representing the structure of the page.
        """

        self.node_class_map = Datasource(
            self._name + ".node_class_map",
            _process_node_class_map, depends_on=[self.wikicode]
        )
        """
        A map of mwparserfromhell.wikicode.<class> to lists of nodes of
        that type.
        """

        self.content = execute_method(
            "strip_code", self.wikicode,
            name=self._name + ".content"
        )
        """
        The viewable content (no markup or templates) of the revision.
        """

        self.headings = get_key(
            mwparserfromhell.nodes.Heading, self.node_class_map,
            default=[],
            name=self._name + ".headings"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Heading`'s
        """

        self.heading_titles = mappers.map(
            _extract_heading_title, self.headings,
            name=self._name + ".heading_titles"
        )
        """
        A list of heading titles
        """

        self.external_links = get_key(
            mwparserfromhell.nodes.ExternalLink, self.node_class_map,
            default=[],
            name=self._name + ".external_links"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.ExternalLink`'s
        """

        self.external_link_urls = mappers.map(
            _extract_external_link_url, self.external_links,
            name=self._name + ".external_link_url"
        )
        """
        A list of external link urls
        """

        self.wikilinks = get_key(
            mwparserfromhell.nodes.Wikilink, self.node_class_map,
            default=[],
            name=self._name + ".wikilinks"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Wikilink`'s
        """

        self.wikilink_titles = mappers.map(
            _extract_wikilink_title, self.wikilinks,
            name=self._name + ".wikilink_titles"
        )
        """
        Returns a list of string titles of internal links (aka "targets")
        """

        self.tags = get_key(
            mwparserfromhell.nodes.Tag, self.node_class_map,
            default=[],
            name=self._name + ".tags"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Tag`'s
        """

        self.tag_names = mappers.map(
            _extract_tag_name, self.tags,
            name=self._name + ".tag_names"
        )
        """
        Returns a list of html tag names present in the content of the revision
        """

        self.tags_str = mappers.map(
            str, self.tags,
            name=self._name + ".tags_str"
        )
        """
        Returns a list of tags present in the content of the revision as strings
        """

        self.templates = get_key(
            mwparserfromhell.nodes.Template, self.node_class_map,
            default=[],
            name=self._name + ".templates"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Templates`'s
        """

        self.template_names = mappers.map(
            _extract_template_name, self.templates,
            name=self._name + ".template_names"
        )
        """
        Returns a list of template names present in the content of the revision
        """

        self.templates_str = mappers.map(
            str, self.templates,
            name=self._name + ".templates_str"
        )
        """
        Returns a list of templates present in the content of the revision as strings
        """
        self.sections = Datasource(
            self._name + ".section",
            _extract_sections, depends_on=[self.wikicode]
        )
        """
        Returns list of sections in the article as wikicode shared node list
        """

    def heading_titles_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list` of
        all header titles that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        if name is None:
            name = "{0}({1})".format(self._name + ".heading_titles_matching",
                                     regex.pattern)
        return filters.regex_matching(regex, self.heading_titles, name=name)

    def headings_by_level(self, level, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that generates a `list` of
        all headers of a level.
        """
        if name is None:
            name = "{0}({1})".format(self._name + ".headings_by_level",
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
                   .format(self._name + ".external_link_urls_matching",
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
                   .format(self._name + ".wikilink_titles_matching",
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
                   .format(self._name + ".tag_names_matching", regex.pattern)

        return filters.regex_matching(regex, self.tag_names, name=name)

    def tags_str_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all tags
        that matches a regular expression as strings.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".tags_str_matching", regex.pattern)

        return filters.regex_matching(regex, self.tags_str, name=name)

    def template_names_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all template
        names that match a regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                   .format(self._name + ".template_names_matching",
                           regex.pattern)

        return filters.regex_matching(regex, self.template_names, name=name)

    def templates_str_matching(self, regex, name=None):
        """
        Constructs a :class:`revscoring.Datasource` that returns all templates
        that matches a regular expression as strings.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)

        if name is None:
            name = "{0}({1})" \
                .format(self._name + ".templates_str_matching",
                        regex.pattern)

        return filters.regex_matching(regex, self.templates_str, name=name)


def _process_wikicode(text):
    return mwparserfromhell.parse(text)


def _process_node_class_map(wikicode):
    node_class_map = {}
    for node in wikicode.filter():
        cls = node.__class__
        if cls in node_class_map:
            node_class_map[cls].append(node)
        else:
            node_class_map[cls] = [node]

    return node_class_map


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


def _extract_sections(wikicode):
    return wikicode.get_sections(flat=True)


class HeadingOfLevel:
    def __init__(self, level):
        self.level = int(level)

    def filter(self, heading):
        return heading.level == self.level


class get_key(Datasource):
    def __init__(self, key, dict_datasource, default=None, name=None):
        self.key = key
        self.default = default
        name = self._format_name(name, [dict_datasource])
        super().__init__(name, self.process, depends_on=[dict_datasource])

    def process(self, d):
        return d.get(self.key, self.default)


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
