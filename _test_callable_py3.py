
import asyncio
from callable import Callable
from signature import signature

import pytest


def f1(a: int, b: str = 'x') -> None:
    pass


@asyncio.coroutine
def f2(a: int, b: str = 'x') -> None:
    pass


@pytest.mark.parametrize('f,sig', [
    (lambda: None, 'lambda'),
    (lambda a, b: None, 'lambda a, b'),
    (lambda a, b, *args: None, 'lambda a, b, *args'),
    (lambda a, b='x', *args, **kw: None, "lambda a, b='x', *args, **kw"),
    (lambda a, b, *args, c=10, **kw: None, 'lambda a, b, *args, c=10, **kw'),
    (lambda a, b='x', *args, c=10, **kw: None, "lambda a, b='x', *args, c=10, **kw"),
    (f1, "def f1(a:int, b:str='x') -> None"),
    (f2, "def f2(a:int, b:str='x') -> None"),
])
def test_signature_py3(f, sig):
    s = signature(f)
    assert s == sig, s


@pytest.mark.parametrize('f,args,kwargs,merged', [
    (lambda x, *args, y=10, **kw: None, (1,), {}, dict(x=1, args=(), y=10, kw={})),
    (lambda x, *, y, z=20: None, (1,), dict(y=10), dict(x=1, y=10, z=20)),
])
def test_kwargify_py3(f, args, kwargs, merged):
    kwargified = Callable(f).kwargify(args, kwargs)
    assert kwargified == merged


@pytest.mark.parametrize('f,args,kwargs,exc', [
    (lambda x, *args, y=30: None, (2), {'x': 1}, TypeError),
    (lambda x, *, y, z=20: None, (1,), {}, TypeError),
])
def test_kwargify_exc_py3(f, args, kwargs, exc):
    with pytest.raises(exc):
        Callable(f).kwargify(args, kwargs)
