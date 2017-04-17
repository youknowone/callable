
import sys
import pytest

from callable import Callable
from signature import signature


if sys.version_info[0] >= 3:
    from _test_callable_py3 import *

@pytest.mark.parametrize('f,sig', [
    (lambda: None, 'lambda'),
    (lambda a, b: None, 'lambda a, b'),
    (lambda a, b, *args: None, 'lambda a, b, *args'),
    (lambda a, b='x', *args, **kw: None, "lambda a, b='x', *args, **kw"),
])
def test_signature_py2(f, sig):
    assert signature(f) == sig, sig


def test_default():
    f = lambda a, b='x': None
    s = Callable(f).arguments
    a = s.get('a')
    assert not a.has_default
    b = s.get('b')
    assert b.has_default
    assert b.default == 'x'
