
from revscoring.datasources import Datasource, revision_oriented
from revscoring.extractors.extractor import Extractor, OfflineExtractor


def get_last_two(id):
    return int(str(id)[-2:])


def test_offline_extractor():
    last_two_in_id = Datasource("last_two_in_id", get_last_two,
                                depends_on=[revision_oriented.revision.id])

    extractor = OfflineExtractor()

    assert extractor.extract(345678, last_two_in_id) == 78

    assert (list(extractor.extract([345678, 4634800], last_two_in_id)) ==
            [(None, 78), (None, 0)])

    extraction_profile = {}
    list(extractor.extract([345678, 4634800], last_two_in_id,
                           profile=extraction_profile))
    assert len(extraction_profile) == 1
    assert len(extraction_profile[last_two_in_id]) == 2


def test_from_config():
    config = {
        'extractors': {
            'enwiki': {
                'class': "revscoring.extractors.api.Extractor",
                'host': "https://en.wikipedia.org",
                'api_path': "/w/api.php",
                'timeout': 20,
                'user_agent': "revscoring tests"
            },
            'offline': {
                'class': "revscoring.extractors.OfflineExtractor"
            }
        }
    }
    Extractor.from_config(config, 'enwiki')
    Extractor.from_config(config, 'offline')

    config = {
        'extractors': {
            'offline': {
                'module': "revscoring.extractors.OfflineExtractor",
            }
        }
    }
    assert Extractor.from_config(config, 'offline') == OfflineExtractor
