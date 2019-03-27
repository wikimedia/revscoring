from revscoring.datasources import Datasource


class Revision:

    def __init__(self, prefix, revision_datasources):

        self.bytes = Datasource(
            prefix + ".bytes", _process_bytes,
            depends_on=[revision_datasources.text]
        )

        if hasattr(revision_datasources, "parent"):
            self.parent = Revision(
                prefix + ".parent",
                revision_datasources.parent
            )


def _process_bytes(text):
    return bytes(text, 'utf-8', 'replace')
