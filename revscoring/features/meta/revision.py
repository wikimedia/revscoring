import re

from ..datasources import revision
from ..feature import Feature


class comment_matches(Feature):
    """
    Returns True if the revision comment matches a regular expression

    :Parameters:
        regex : `str`
            A regular expression to apply to the comment
        name : `str`
            A name to associate with the feature.  If not set, the feature's
            name will be 'comment_matches(<regex>)'
    """
    def __init__(self, regex, name=None):
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        self.regex = regex

        if name is None:
            name = "comment_matches({0})".format(repr(regex))
        super().__init__(name, self._process, returns=bool,
                         depends_on=[revision.comment])

    def _process(self, comment):
        return bool(re.match(self.regex, comment))


class internal_links_matching(Feature):
    """
    Returns a count of the number of internal links with targets that match
    a regular expression.

    :Parameters:
        regex : `str`
            A regular expression to apply to the link targets
        name : `str`
            A name to associate with the feature.  If not set, the feature's
            name will be 'internal_links_matching(<regex>)'
    """
    def __init__(self, regex, name=None):
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        self.regex = regex

        if name is None:
            name = "internal_links_matching({0})".format(repr(regex))
        super().__init__(name, self._process, returns=int,
                         depends_on=[revision.internal_links])

    def _process(self, internal_links):
        return sum(bool(re.match(self.regex, str(link.title)))
                   for link in internal_links)


class templates_matching(Feature):
    """
    Returns a count of the number of templates with names that match
    a regular expression.
    
    :Parameters:
        regex : `str`
            A regular expression to apply to the link targets
        name : `str`
            A name to associate with the feature.  If not set, the feature's
            name will be 'internal_links_matching(<regex>)'
    """
    def __init__(self, regex, name=None):
        if not hasattr(regex, "pattern"):
            regex = re.compile(regex, re.I)
        self.regex = regex

        if name is None:
            name = "{0}({1})".format(self.__class__.__name__, regex.pattern)

        super().__init__(name, self._process, depends_on=[revision.templates],
                         returns=int)

    def _process(self, templates):
        return sum(bool(self.regex.match(str(template.name).replace("_", " ")))
                   for template in templates)
