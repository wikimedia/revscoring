from nose.tools import eq_

from ..dependencies import depends
from ..returns import returns


def test_returns():
    
    @returns(int)
    def test(): return 1
    
    eq_(test.return_type, int)
    
    @depends(on=["foo"])
    @returns(int)
    def test2(): return 1
    
    eq_(test2.return_type, int)
    eq_(test2.dependencies, ["foo"])
