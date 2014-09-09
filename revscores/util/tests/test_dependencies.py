from nose.tools import eq_, raises

from ..dependencies import DependencyLoop, depends, solve


def test_depends():
    
    @depends(on=["bar"])
    def foo(bar):
        return 1
        
    
    eq_(foo.dependencies, ["bar"])
    assert callable(foo)

def test_solve():
    
    @depends(on=["bar"])
    def foo(bar):
        return bar * 5
    
    @depends(on=[foo])
    def herp(foo):
        return "Herp value: {0}".format(foo)
    
    cache = {"bar": 1}
    
    eq_(solve(herp, cache), "Herp value: 5")

@raises(DependencyLoop)
def test_solve_loop():
    
    @depends()
    def foo(bar):
        return bar + 1
    
    @depends(on=[foo])
    def bar(foo):
        return foo + 1
        
    foo.dependencies.append(bar)
    
    solve(foo)
