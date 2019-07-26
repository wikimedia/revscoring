
from revscoring.datasources import Datasource
from revscoring.features.feature import Constant, Feature
from revscoring.features.feature_vector import FeatureVector
from revscoring.features.functions import trim, vectorize_values
from revscoring.features.modifiers import log, max


def test_trim():

    d1 = Datasource("derp1")
    f1 = Feature("foobar1", returns=int)
    f2 = Feature("foobar2", returns=int, depends_on=[d1])
    c = Constant(value=5)
    fv = FeatureVector("foobar3", returns=int, depends_on=[c])

    assert list(trim(f1)) == [f1]
    assert list(trim([f1, f2, fv])) == [f1, f2, fv]
    assert list(trim([f1, f2, f1 + f2, fv])) == [f1, f2, fv]
    assert (list(trim(log(max(f1 - f2, 1)))) ==
            [f1, f2])


def test_vectorize_features():

    feature_values = [1, 2.0, [1.0, 2.0, 3.0], False]
    assert (vectorize_values(feature_values) ==
            [1, 2.0, 1.0, 2.0, 3.0, False])
