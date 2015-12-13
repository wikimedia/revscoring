class NamedDict(dict):
    def __init__(self, **kwargs):
        for attr, value in kwargs.items():
            self[attr] = value

    def __getattr__(self, attr):
        return self[attr]

    def __setattr__(self, attr, value):
        self[attr] = value
