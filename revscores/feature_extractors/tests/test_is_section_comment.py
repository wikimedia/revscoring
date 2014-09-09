from nose.tools import eq_

from ...datasources import RevisionMetadata
from ..is_section_comment import is_section_comment


def test_is_section_comment():
    rm = RevisionMetadata(None,
                          None,
                          None,
                          None,
                          None,
                          "/* Foobar */ I did some stuff!",
                          None,
                          None,
                          None,
                          None,
                          None)
    
    assert is_section_comment(rm)
    
    rm = RevisionMetadata(None,
                          None,
                          None,
                          None,
                          None,
                          "Derp some stuff!",
                          None,
                          None,
                          None,
                          None,
                          None)
    
    assert not is_section_comment(rm)
