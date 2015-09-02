from ..datasources import page_creation, revision, site
from .feature import Feature


def process_is_content_namespace(revision_metadata, namespace_map):
    return namespace_map[revision_metadata.page_namespace].content

is_content_namespace = \
    Feature("page.is_content_namespace", process_is_content_namespace,
            returns=bool,
            depends_on=[revision.metadata, site.namespace_map])
"""
Represents whether this page is in a content namespace or not.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import page
        >>> list(extractor.extract(655097130, [page.is_content_namespace]))
        [True]
"""


def process_is_mainspace(revision_metadata):
    return revision_metadata.page_namespace == 0

is_mainspace = Feature("page.is_mainspace", process_is_mainspace,
                       returns=bool,
                       depends_on=[revision.metadata])
"""
Represents whether this page is in main namespace or not.

:Returns:
    bool

:Example:
    ..code-block:: python

        >>> from revscoring.features import page
        >>> list(extractor.extract(655097130, [page.is_mainspace]))
        [True]
"""


def process_age(page_creation_metadata, revision_metadata):
    return revision_metadata.timestamp - page_creation_metadata.timestamp

age = Feature("page.age", process_age,
              returns=int,
              depends_on=[page_creation.metadata, revision.metadata])
"""
Represents age of the page in seconds when this edit made.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import page
        >>> list(extractor.extract(655097130, [page.age]))
        [413618413]
"""
