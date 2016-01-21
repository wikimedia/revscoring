from ..extractor import Extractor


def test_from_config():
    config = {
        'extractors': {
            'enwiki': {
                'host': "https://en.wikipedia.org",
                'api_path': "/w/api.php",
                'timeout': 20,
                'user_agent': "revscoring tests"
            }
        }
    }

    Extractor.from_config(config, 'enwiki')  # Doesn't error
