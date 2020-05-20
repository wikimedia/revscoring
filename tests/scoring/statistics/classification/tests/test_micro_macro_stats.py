from collections import OrderedDict

from revscoring.scoring.statistics.classification.micro_macro_stats import \
    MicroMacroStats
from revscoring.scoring.statistics.classification.scaled_prediction_statistics import \
    ScaledPredictionStatistics as SPS # noqa


def test_micro_macro_stats():
    # (tp, fp, tn, fn)
    stats_keys = ['Short', 'Labels', 'Can', 'Be', 'Columns']
    stats_values = [
        SPS(counts=(10, 2, 5, 8)),
        SPS(counts=(9, 3, 9, 4)),
        SPS(counts=(11, 1, 8, 5)),
        SPS(counts=(10, 2, 9, 4)),
        SPS(counts=(5, 7, 3, 10))
    ]
    stats = OrderedDict()
    for key, value in zip(stats_keys, stats_values):
        stats[key] = value
    mms = MicroMacroStats(stats, 'precision')

    print(mms.format_str({}))
    assert len(mms.format_str({}).split('\n')) <= 5
    assert list(stats.keys()) == list(mms['labels'].keys())

    # (tp, fp, tn, fn)
    stats = {
        'A really long label name': SPS(counts=(10, 2, 5, 8)),
        'Another long label name': SPS(counts=(9, 3, 9, 4)),
        'Again we\'re very long': SPS(counts=(11, 1, 8, 5)),
        'We should be too long': SPS(counts=(10, 2, 9, 4)),
        'One more for good measure': SPS(counts=(5, 7, 3, 10))
    }
    mms = MicroMacroStats(stats, 'precision')

    print(mms.format_str({}))
    assert len(mms.format_str({}).split('\n')) > 5
