from revscoring import Feature, FeatureVector
from revscoring.dependencies import solve
from revscoring.features.meta import operators

int_1 = Feature("int_1", returns=int)
int_2 = Feature("int_2", returns=int)
bool_1 = Feature("bool_1", returns=bool)
bool_2 = Feature("bool_2", returns=bool)
int_vector_1 = FeatureVector("int_vector_1", returns=int)
int_vector_2 = FeatureVector("int_vector_2", returns=int)
bool_vector_1 = FeatureVector("bool_vector_1", returns=bool)
bool_vector_2 = FeatureVector("bool_vector_2", returns=bool)


def test_singleton():
    cache = {int_1: 1, int_2: 2}
    assert solve(operators.add(int_1, int_2), cache=cache) == 3
    assert solve(operators.sub(int_1, int_2), cache=cache) == -1
    assert solve(operators.mul(int_1, int_2), cache=cache) == 2
    assert solve(operators.div(int_1, int_2), cache=cache) == 0.5

    assert solve(operators.eq(int_1, int_2), cache=cache) is False
    assert solve(operators.ne(int_1, int_2), cache=cache) is True
    assert solve(operators.le(int_1, int_2), cache=cache) is True
    assert solve(operators.lt(int_1, int_2), cache=cache) is True
    assert solve(operators.ge(int_1, int_2), cache=cache) is False
    assert solve(operators.gt(int_1, int_2), cache=cache) is False

    cache = {bool_1: True, bool_2: False}
    assert solve(operators.and_(bool_1, bool_2), cache=cache) is False
    assert solve(operators.or_(bool_1, bool_2), cache=cache) is True
    assert solve(operators.not_(bool_1), cache=cache) is False
    assert solve(operators.not_(bool_2), cache=cache) is True


def test_vector():
    cache = {int_vector_1: [1, 2, 1, 3], int_vector_2: [2, 1, 1, -1]}
    assert solve(operators.add(int_vector_1, int_vector_2), cache=cache) == [3, 3, 2, 2]
    assert solve(operators.sub(int_vector_1, int_vector_2), cache=cache) == [-1, 1, 0, 4]
    assert solve(operators.mul(int_vector_1, int_vector_2), cache=cache) == [2, 2, 1, -3]
    assert solve(operators.div(int_vector_1, int_vector_2), cache=cache) == [0.5, 2, 1, -3]

    assert solve(operators.eq(int_vector_1, int_vector_2), cache=cache) == [False, False, True, False]
    assert solve(operators.ne(int_vector_1, int_vector_2), cache=cache) == [True, True, False, True]
    assert solve(operators.le(int_vector_1, int_vector_2), cache=cache) == [True, False, True, False]
    assert solve(operators.lt(int_vector_1, int_vector_2), cache=cache) == [True, False, False, False]
    assert solve(operators.ge(int_vector_1, int_vector_2), cache=cache) == [False, True, True, True]
    assert solve(operators.gt(int_vector_1, int_vector_2), cache=cache) == [False, True, False, True]

    cache = {bool_vector_1: [True, False, True, False], bool_vector_2: [True, True, False, False]}
    assert solve(operators.and_(bool_vector_1, bool_vector_2), cache=cache) == [True, False, False, False]
    assert solve(operators.or_(bool_vector_1, bool_vector_2), cache=cache) == [True, True, True, False]
    assert solve(operators.not_(bool_vector_1), cache=cache) == [False, True, False, True]
    assert solve(operators.not_(bool_vector_2), cache=cache) == [False, False, True, True]
