
import asyncio
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
