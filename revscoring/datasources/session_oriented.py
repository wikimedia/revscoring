"""
Implements a set of datasources oriented off of a single revision.  This is
useful for extracting features of edit and article quality.

.. autodata:: revscoring.datasources.session_oriented.session

Supporting classes
++++++++++++++++++

.. autoclass:: revscoring.datasources.session_oriented.Session
    :members:
    :member-order: bysource

Supporting functions
++++++++++++++++++++

.. autofunction:: revscoring.datasources.session_oriented.list_of_tree

.. autofunction:: revscoring.datasources.session_oriented.list_of_ify
"""
import logging
import re
from functools import wraps
from inspect import getmembers, ismethod

from revscoring import Feature, FeatureVector
from revscoring.features.meta import expanders as feature_expanders

from ..dependencies import DependentSet
from .datasource import Datasource
from .meta import expanders as datasource_expanders
from .revision_oriented import Revision, User

logger = logging.getLogger(__name__)


def list_of_tree(dependent_set, rewrite_name=None, cache=None):
    """
    Converts a :class:`~revscoring.DependentSet` and all of the
    :class:`~revscoring.Dependent` named into a new
    :class:`~revscoring.DependentSet` with
    :func:`~revscoring.datasources.session_oriented.list_of_ify` applied.

    :Parameters:
        dependent_set : :class:`~revscoring.DependentSet`
            A dependent set to convert
        rewrite_name : function
            A function to apply to the dependent's name when re-creating it.
        cache : dict(:class:`~revscoring.Feature` | :class:`~revscoring.FeatureVector` | :class:`~revscoring.Datasource`)
            A map of dependents that have already been converted.
    """
    logger.debug("Applying list_of_tree to {0}".format(dependent_set.name))
    cache = cache if cache is not None else {}
    rewrite_name = rewrite_name if rewrite_name is not None else \
        lambda name: name

    # Rewrites all dependents.
    for attr, dependent in dependent_set.dependents.items():
        new_dependent = list_of_ify(dependent, rewrite_name, cache)
        setattr(dependent_set, attr, new_dependent)

    # Iterate into all sub-DependentSets
    for attr, sub_dependent_set in dependent_set.dependent_sets.items():
        if attr.startswith("_"):
            pass
        else:
            logger.debug("Running list_of_tree on {0}".format(attr))
            new_dependent_set = list_of_tree(
                sub_dependent_set, rewrite_name, cache)
            setattr(dependent_set, attr, new_dependent_set)

    # Iterate into all meta-dependents (methods that return a new dependent)
    for attr, method in getmembers(dependent_set, ismethod):
        if not hasattr(method, "meta_dependent"):
            pass
        else:
            list_of_meta_method = meta_list_of_ify(
                method, rewrite_name, cache)
            setattr(dependent_set, attr, list_of_meta_method)

    return dependent_set


def list_of_ify(dependent, rewrite_name, cache):
    """
    Converts any :class:`~revscoring.Feature`,
    :class:`~revscoring.FeatureVector`, or :class:`~revscoring.Datasource` into
    an equivalent "list of" the same dependent.  Dependencies are converted
    recursively and a cache is maintained for memoization.

    :Parameters:
        dependent : (:class:`~revscoring.Feature` | :class:`~revscoring.FeatureVector` | :class:`~revscoring.Datasource`)
            A dependent to convert
        rewrite_name : function
            A function to apply to the dependent's name when re-creating it.
        cache : dict(:class:`~revscoring.Feature` | :class:`~revscoring.FeatureVector` | :class:`~revscoring.Datasource`)
            A map of dependents that have already been converted.
    """

    new_name = rewrite_name(dependent.name)
    if new_name in cache:
        logger.debug("list_of_ify {0} in the cache".format(dependent.name))
        return cache[new_name]
    else:
        logger.debug("list_of_ify is modifying {0} into a list_of".format(dependent.name))
        new_dependencies = [list_of_ify(dependency, rewrite_name, cache)
                            for dependency in dependent.dependencies]

        if isinstance(dependent, Datasource):
            new_dependent = datasource_expanders.list_of(
                dependent, depends_on=new_dependencies, name=new_name)
        elif isinstance(dependent, FeatureVector):
            new_dependent = datasource_expanders.list_of(
                dependent, depends_on=new_dependencies, name=new_name)
        elif isinstance(dependent, Feature):
            new_dependent = feature_expanders.list_of(
                dependent, depends_on=new_dependencies, name=new_name)
        else:
            raise TypeError("Cannot convert type {0} into a list_of"
                            .format(type(dependent)))

        cache[new_name] = new_dependent
        return cache[new_name]


def meta_list_of_ify(method, rewrite_name, cache):
    @wraps(method)
    def wrapper(*args, **kwargs):
        dependent = method(*args, **kwargs)
        return list_of_ify(dependent, rewrite_name, cache)

    return wrapper


def rewrite_name(name):
    return re.sub(r"(^|\.)revision\.", r"\1session.revisions.", name)


class Session(DependentSet):
    """
    Represents a session -- an ordered list of revisions
    """
    def __init__(self, name):
        super().__init__(name)
        self.revisions = list_of_tree(Revision(
            "session.revisions",
            include_page_creation=True,
            include_content=True,
            include_user=False,
            include_page_suggested=True),
            rewrite_name=rewrite_name)
        """
        :class:`revscoring.datasources.revision_oriented.Revision`: modified by
        :func:`~revscoring.datasources.session_oriented.list_of_tree()`
        """

        self.user = User(
            name + ".user",
            include_info=True,
            include_last_revision=True
        )
        """
        :class:`revscoring.datasources.revision_oriented.User`
        """

session = Session("session")
"""
Represents the session of interest.  Implements this structure:

* session: :class:`~revscoring.datasources.session_oriented.Session`
    * revisions: :class:`~revscoring.datasources.revision_oriented.Revision`
        * diff: :class:`~revscoring.datasources.revision_oriented.Diff`
        * page: :class:`~revscoring.datasources.revision_oriented.Page`
            * namespace: :class:`~revscoring.datasources.revision_oriented.Namespace`
            * creation: :class:`~revscoring.datasources.revision_oriented.Revision`
        * parent: :class:`~revscoring.datasources.revision_oriented.Revision`
            * user: :class:`~revscoring.datasources.revision_oriented.User`
    * user: :class:`~revscoring.datasources.revision_oriented.User`
        * info: :class:`~revscoring.datasources.revision_oriented.UserInfo`
        * last_revision: :class:`~revscoring.datasources.revision_oriented.Revision`
"""  # noqa
