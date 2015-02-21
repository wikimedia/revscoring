from io import BytesIO
from pprint import pprint

from revscoring.features import (proportion_of_badwords_added,
                                 proportion_of_markup_added)
from revscoring.scorers import LinearSVCModel, MLScorerModel

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

model = LinearSVCModel([proportion_of_badwords_added,
                        proportion_of_markup_added])

print("Training classifier")
pprint(model.train(training_set))
print("")
print("Testing classifier")
pprint(model.test(test_set))
print("")
print("Making a prediction")
pprint(model.score([2.4, 2.1]))

f = BytesIO()
model.dump(f)

f.seek(0)
model = MLScorerModel.load(f)
