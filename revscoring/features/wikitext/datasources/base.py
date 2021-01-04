from revscoring.dependencies import DependentSet


class BaseRevision(DependentSet):

    def __init__(self, name, revision_datasources):
        super().__init__(name)
        self.text = revision_datasources.text


class BaseDiff(DependentSet):

    def __init__(self, name, revision):
        super().__init__(name)
        self.revision = revision
