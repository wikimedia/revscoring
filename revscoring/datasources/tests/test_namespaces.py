from nose.tools import eq_

from ..namespaces import namespaces


def test_namespaces():
    
    fake_si_doc = {
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
    
    nses = namespaces(fake_si_doc)
    
    eq_(len(nses), 3)
    eq_(sum(ns.content for ns in nses.values()), 1)
