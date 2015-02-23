from ..dependent import Dependent, solve_many


class Language:
    def __init__(self, name, utilities):
        self.name = str(name)
        self.utilities = list(utilities)
    
    def cache(self):
        utility_methods = zip(self.utilities, solve_many(self.utilities))
        return {utility:method for utility, method in utility_methods}
        

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
stem_word = LanguageUtility("stem_word")
is_badword = LanguageUtility("is_badword")
is_misspelled = LanguageUtility("is_misspelled")
is_stopword = LanguageUtility("is_stopword")
