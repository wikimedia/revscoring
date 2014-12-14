from revscores.scorers import LinearSVC
from revscores.util.returns import returns

returns(float)
def fake_feature1():
    return 5.0

returns(float)
def fake_feature2():
    return 0.1


training_set = [
    ([10.1, 20.1], 1),
    ([19.2, 15.3], 1),
    ([13.1, 12.5], 1),
    ([0.5, 0.6], 0),
    ([2.4, 0.1], 0),
    ([0.9, 3.1], 0)
]
test_set = [
    ([13.1, 12.1], 1),
    ([9.2, 19.3], 1),
    ([12.1, 14.5], 1),
    ([19.5, 19.6], 0),
    ([2.4, 2.1], 0),
    ([0.1, 3.1], 0)
]

linear_svc_model = LinearSVC.MODEL([fake_feature1,fake_feature2])
linear_svc_model.train(training_set)
print(linear_svc_model.test(test_set))
