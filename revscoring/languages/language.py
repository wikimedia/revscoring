import yamlconf

from .. import dependencies


class Language(dependencies.Context):
    def __init__(self, name, utilities):
        super().__init__(context=utilities)
        self.name = str(name)

    def __eq__(self, other):
        try:
            return self.name == other.name and \
                   self.context == other.context
        except AttributeError as e:
            return False

    @classmethod
    def from_config(self, config, name, section_key="languages"):
        section = config[section_key][name]
        if 'module' in section:
            return yamlconf.import_module(section['module'])
        elif 'class' in section:
            raise RuntimeError("Loading a language via class construction " + \
                               "not yet supported")


class LanguageUtility(dependencies.Dependent):
    pass

# Define placeholder utilities.  These will need to be replaced inside of a
# language, but they will provide names to match against within the cache.
stem_word = LanguageUtility("stem_word")
is_badword = LanguageUtility("is_badword")
is_misspelled = LanguageUtility("is_misspelled")
is_stopword = LanguageUtility("is_stopword")
