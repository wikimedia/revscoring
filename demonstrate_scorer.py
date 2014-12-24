from io import BytesIO
from pprint import pprint

from revscores.features import (proportion_of_badwords_added,
                                proportion_of_markup_added)
from revscores.scorers import LinearSVC

training_set = [
    ([10.1, 20.1], True),
    ([19.2, 15.3], True),
    ([13.1, 12.5], True),
    ([0.5, 0.6], False),
    ([2.4, 0.1], False),
    ([0.9, 3.1], False)
]
test_set = [
    ([13.1, 12.1], True),
    ([9.2, 19.3], True),
    ([12.1, 14.5], True),
    ([19.5, 19.6], False),
    ([2.4, 2.1], False),
    ([0.1, 3.1], False)
]

linear_svc_model = LinearSVC.MODEL([proportion_of_badwords_added,
                                    proportion_of_markup_added])

print("Training classifier")
pprint(linear_svc_model.train(training_set))
print("")
print("Testing classifier")
pprint(linear_svc_model.test(test_set))

f = BytesIO()
linear_svc_model.dump(f)

f.seek(0)
linear_svc_model = LinearSVC.MODEL.load(f)
