class DictDiff:
    """
    Represents the difference between two dictionaries
    """
    __slots__ = ('added', 'removed', 'intersection', 'changed', 'unchanged')

    def __init__(self, added, removed, intersection, changed, unchanged):
        self.added = added
        """
        `set` ( `mixed` ) : Keys that were added in the new dictionary
        """

        self.removed = removed
        """
        `set` ( `mixed` ) : Keys that were removed in the new dictionary
        """

        self.intersection = intersection
        """
        `set` ( `mixed` ) : Keys that appear in both dictionaries
        """

        self.changed = changed
        """
        `set` ( `mixed` ) : Keys that appear in both dictionaries, but the
                            values differ
        """

        self.unchanged = unchanged
        """
        `set` ( `mixed` ) : Keys that appear in both dictionaries and have
                            equivalent values
        """


def diff_dicts(a, b):
    """
    Generates a diff between two dictionaries.

    :Parameters:
        a : `dict`
            A dict to diff or `None`
        b : `dict`
            B dict to diff
    """
    a = a or {}
    added = b.keys() - a.keys()
    removed = a.keys() - b.keys()
    intersection = a.keys() & b.keys()

    changed = set()
    unchanged = set()
    for key in intersection:
        if a[key] == b[key]:
            unchanged.add(key)
        else:
            changed.add(key)

    return DictDiff(added, removed, intersection, changed, unchanged)
