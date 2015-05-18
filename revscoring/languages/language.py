import yamlconf

from ..dependent import Dependent, solve_many


class Language:
    def __init__(self, name, utilities):
        self.name = str(name)
        self.utilities = list(utilities)

    def __eq__(self, other):
        try:
            return self.name == other.name and \
                   self.utilities == other.utilities
        except AttributeError as e:
            return False

    def context(self):
        return {u:u for u in self.utilities}

    def cache(self):
        return {u:u() for u in self.utilities}

    @classmethod
    def from_config(self, config, name, section_key="languages"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            raise RuntimeError("Loading a language via class construction " + \
                               "not yet supported")


def not_implemented_processor():
    raise NotImplementedError()

class LanguageUtility(Dependent):

    def __init__(self, name, processor=None, depends_on=None):
        depends_on = depends_on or []
        processors = processor or not_implemented_processor

        super().__init__(name, processor, dependencies=depends_on)

    def __hash__(self):
        return hash((self.__class__.__name__, self.name))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

# Define placeholder utilities.  These will need to be replaced inside of a
# language, but they will provide names to match against within the cache.
stem_word = LanguageUtility("stem_word", not_implemented_processor)
is_badword = LanguageUtility("is_badword", not_implemented_processor)
is_misspelled = LanguageUtility("is_misspelled", not_implemented_processor)
is_stopword = LanguageUtility("is_stopword", not_implemented_processor)
