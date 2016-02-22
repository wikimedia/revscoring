def fpr_score(y_true, y_pred):
    true_preds = sum(y_pred) or 1
    return sum(yp and not yt for yt, yp in zip(y_true, y_pred)) / true_preds


def filter_rate_score(y_pred):
    return 1 - (sum(y_pred) / len(y_pred))


def round_or_none(value, ndigits):
    if value is None:
        return None
    else:
        return round(value, ndigits)


def round_floats(d, digits=0):
    new_d = {}
    for key, value in d.items():
        if isinstance(value, float):
            value = round(value, digits)
        elif isinstance(value, dict):
            value = round_floats(value, digits=digits)
        new_d[key] = value
    return new_d
