import pickle

from revscoring.datasources import revision_oriented as ro
from revscoring.dependencies import solve
from revscoring.features.wikitext import revision


def test_extract_sections():
