from ..micro_macro_stats import MicroMacroStats
from ..scaled_prediction_statistics import ScaledPredictionStatistics as SPS


def test_micro_macro_stats():
    # (tp, fp, tn, fn)
    stats = {
        'Short': SPS(counts=(10, 2, 5, 8)),
        'Labels': SPS(counts=(9, 3, 9, 4)),
        'Can': SPS(counts=(11, 1, 8, 5)),
        'Be': SPS(counts=(10, 2, 9, 4)),
        'Columns': SPS(counts=(5, 7, 3, 10))
    }
    mms = MicroMacroStats(stats, 'precision')

    print(mms.format_str({}))
    assert len(mms.format_str({}).split('\n')) <= 5

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
