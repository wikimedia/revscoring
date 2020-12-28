from revscoring.dependencies import DependentSet


class BaseRevision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.datasources = revision_datasources


class BaseDiff(DependentSet):

    def __init__(self, name, diff_datasources, *args, **kwargs):
        super().__init__(name)
        self.datasources = diff_datasources
