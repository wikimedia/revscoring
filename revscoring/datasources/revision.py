from .datasource import Datasource

id = Datasource("revision.id")
"""
Returns the `rev_id` of the current revision.
"""

metadata = Datasource("revision.metadata")
"""
Returns a `dict` of metadata for the current revision.
"""

text = Datasource("revision.text")
"""
Returns the text content of the current revision.
"""


def process_comment(metadata):
    return metadata['comment']

comment = Datasource("revision.comment", process_comment,
                     depends_on=[metadata])
"""
Returns the comment saved with the revision.
"""
