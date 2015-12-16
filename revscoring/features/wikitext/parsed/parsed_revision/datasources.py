

class Datasources:

    def __init__(self, prefix, text_datasource):
        self.prefix = prefix

        def process_wikicode(text):
            if text is None:
                raise RevisionNotFound()
            return mwparserfromhell.parse(text or "")

        self.wikicode = Datasource(
            prefix + ".wikicode",
            process_wikicode, depends_on=[text_datasource]
        )
        """
        A :class:`mwparserfromhell.wikicode.Wikicode` abstract syntax
        tree representing the content of the revision.
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

        def extract_heading_title(heading):
            return str(heading.title).strip()
        self.heading_titles = map(
            extract_heading_title, self.headings,
            name=prefix + ".heading_titles"
        )
        """
        A list of heading titles
        """

    def heading_titles_matchings(self, regex, name=None, regex_flags=re.I):
        """
        Builds a datasource that represents all header titles that match a
        regular expression.
        """
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, regex_flags)
        if name is None:
            name = "{0}({1})".format(self.prefix + ".heading_titles_matching",
                                     regex.pattern)
        return filters.regex_matching(regex,
                                      self.heading_titles,
                                      name=name)

        self.external_links = execute_method(
            "filter_external_links", self.wikicode,
            name=prefix + ".external_links"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.ExternalLink`'s
        """

        def extract_external_link_url(elink):
            return str(elink.url)
        self.external_link_urls = map(
            extract_external_link_url, self.external_links,
            name=prefix + ".external_link_url"
        )
        """
        A list of external link urls
        """

        def external_link_urls_matching(regex, name=None, regex_flags=re.I):
            """
            A list of external link URLs that match a regular expression
            """
            if not hasattr(regex, "pattern"):
                regex = re.compile(regex, regex_flags)

            if name is None:
                name = "{0}({1})" \
                       .format(prefix + ".external_link_urls_matching",
                               regex.pattern)

            return filters.regex_matching(
                regex, self.external_link_urls, name=name
            )


        self.wikilinks = execute_method(
            "filter_wikilinks", self.wikicode,
            name=prefix + ".wikilinks"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Wikilink`'s
        """


        def extract_internal_link_title(ilink):
            return str(ilink.title)
        self.internal_link_titles = map(
            extract_internal_link_title, internal_links,
            name=prefix + ".internal_link_titles"
        )
        """
        Returns a list of string titles of internal links (aka "targets")
        """


        def internal_link_titles_matching(regex, name=None, regex_flags=re.I):
            if not hasattr(regex, "pattern"):
                regex = re.compile(regex, regex_flags)

            if name is None:
                name = "{0}({1})" \
                       .format(prefix + ".internal_link_titles_matching",
                               regex.pattern)

            return regex_matching(regex, internal_link_titles, name=name)
        """
        Constructs a :class:`revscoring.Datasource` that returns all internal link
        titles names that match a regular expression.
        """


        self.tags = execute_method(
            "filter_tags", self.wikicode,
            name=prefix + ".tags"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Tag`'s
        """


        def extract_tag_name(tag):
            return str(tag.tag)

        self.tag_names = map(extract_tag_name, tags, name=prefix + ".tag_names")
        """
        Returns a list of html tag names present in the content of the revision
        """


        def tag_names_matching(regex, name=None, regex_flags=re.I):
            if not hasattr(regex, "pattern"):
                regex = re.compile(regex, regex_flags)

            if name is None:
                name = "{0}({1})" \
                       .format(prefix + ".tag_names_matching", regex.pattern)

            return regex_matching(regex, tag_names, name=name)
        """
        Constructs a :class:`revscoring.Datasource` that returns all tag names that
        match a regular expression.
        """


        self.templates = execute_method(
            "filter_templates", self.wikicode,
            name=prefix + ".templates"
        )
        """
        A list of :class:`mwparserfromhell.nodes.heading.Templates`'s
        """


        def extract_template_name(template):
            return str(template.name)

        self.template_names = map(
            extract_template_name, templates,
            name=prefix + ".template_names"
        )
        """
        Returns a list of template names present in the content of the revision
        """


        def template_names_matching(regex, name=None, regex_flags=re.I):
            if not hasattr(regex, "pattern"):
                regex = re.compile(regex, regex_flags)

            if name is None:
                name = "{0}({1})" \
                       .format(prefix + ".template_names_matching",
                               regex.pattern)

            return regex_matching(regex, template_names, name=name)
        """
        Constructs a :class:`revscoring.Datasource` that returns all template names
        that match a regular expression.
        """


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
