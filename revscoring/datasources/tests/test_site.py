from nose.tools import eq_

from .. import site
from ...dependent import solve


def test_namespace_map():

    cache = {
        site.doc: {
            "namespaces": {
                "0": {
                    "id": 0,
                    "case": "first-letter",
                    "*": "",
                    "content": ""
                },
                "1": {
                    "id": 1,
                    "case": "first-letter",
                    "*": "Discuss\u00e3o",
                    "subpages": "",
                    "canonical": "Talk"
                },
                "2": {
                    "id": 2,
                    "case": "first-letter",
                    "*": "Usu\u00e1rio(a)",
                    "subpages": "",
                    "canonical": "User"
                }
            },
            "namespacealiases": [
                {
                    "id": 1,
                    "*": "WAFFLES"
                }
            ]
        }
    }

    namespace_map = solve(site.namespace_map, cache=cache)

    eq_(len(namespace_map), 3)
    eq_(sum(ns.content for ns in namespace_map.values()), 1)
