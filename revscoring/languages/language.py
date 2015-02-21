class Language:
    """
    Constructs a Language instance that wraps two functions, "is_badword" and
    "is_misspelled" -- which will check if a word is "bad" or does not appear
    in the dictionary.
    """
    def __init__(self, name, is_badword, is_misspelled):
        self.name = str(name)
        self.is_badword = is_badword
        self.is_misspelled = is_misspelled
    
    def badwords(self, words):
        
        for word in words:
            if self.is_badword(word): yield word
    
    def misspellings(self, words):
        
        for word in words:
            if self.is_misspelled(word): yield word
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not hash(self) == hash(other)
