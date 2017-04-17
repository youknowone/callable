
import sys
print(sys.version_info[0])
if sys.version_info[0] >= 3:
    from _test_callable_py3 import *

from callable import signature

import pytest

@pytest.mark.parametrize('f,sig', [
    (lambda: None, 'lambda'),
    (lambda a, b: None, 'lambda a, b'),
    (lambda a, b, *args: None, 'lambda a, b, *args'),
    (lambda a, b='x', *args, **kw: None, "lambda a, b='x', *args, **kw"),
])
def test_signature_py2(f, sig):
    assert signature(f) == sig, sig

