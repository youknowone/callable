
import sys
import pytest

from callable import Callable, inspect
from signature import signature


if sys.version_info[0] >= 3:
    from _test_callable_py3 import *  # noqa


@pytest.mark.parametrize('f,sig', [
    (lambda: None, 'lambda'),
    (lambda a, b: None, 'lambda a, b'),
    (lambda a, b, *args: None, 'lambda a, b, *args'),
    (lambda a, b='x', *args, **kw: None, "lambda a, b='x', *args, **kw"),
])
def test_signature_py2(f, sig):
    assert signature(f) == sig, (signature(f), sig)


def test_default():
    f = lambda a, b='x': None  # noqa
    s = Callable(f).parameters
    a = s.get('a')
    assert a.default is inspect.Parameter.empty
    b = s.get('b')
    assert b.default is not inspect.Parameter.empty
    assert b.default == 'x'


def test_get():
    c = Callable(test_signature_py2)
    assert c.parameters['f'].default is inspect.Parameter.empty
    with pytest.raises(KeyError):
        c.parameters['xyz']


@pytest.mark.parametrize('f,args,kwargs,merged', [
    (lambda: None, (), {}, {}),
    (lambda x, y: None, (1, 2), {}, dict(x=1, y=2)),
    (lambda x, y, z=30: None, (1, 2), {}, dict(x=1, y=2, z=30)),
    (lambda x, y, z=30: None, (1,), {'y': 2}, dict(x=1, y=2, z=30)),
    (lambda x, y, z=30: None, (1, 2, 3), {}, dict(x=1, y=2, z=3)),
    (lambda x, y, z=30: None, (1,), {'y': 20}, dict(x=1, y=20, z=30)),
    (lambda x, y, *args: None, (1,), {'y': 20}, dict(x=1, y=20, args=())),
    (lambda x, y, *args: None, (1, 2, 3, 4, 5), {}, dict(x=1, y=2, args=(3, 4, 5))),
    (lambda x, **kw: None, (), {'x': 10, 'y': 20, 'z': 30}, dict(x=10, kw={'y': 20, 'z': 30})),
    (lambda x, *args, **kw: None, (1, 2, 3, 4), {'y': 20, 'z': 30}, dict(x=1, args=(2, 3, 4), kw={'y': 20, 'z': 30})),
])
def test_kwargify(f, args, kwargs, merged):
    kwargified = Callable(f).kwargify(args, kwargs)
    print(kwargified)
    print(merged)
    assert kwargified == merged


@pytest.mark.parametrize('f,args,kwargs,exc', [
    (lambda: None, (1, 2), {}, TypeError),
    (lambda x, y: None, (2, 3), {'x': 1}, TypeError),
    (lambda x, y, z=30: None, (1,), {}, TypeError),
    (lambda x, y, z=30: None, (1,), {'x': 2}, TypeError),
])
def test_kwargify_exc(f, args, kwargs, exc):
    with pytest.raises(exc):
        Callable(f).kwargify(args, kwargs)
