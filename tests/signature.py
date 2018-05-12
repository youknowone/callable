
try:
    import inspect2 as inspect
except ImportError:
    import inspect
from callable import Callable


def argument(arg):
    prefixes = {
        inspect.Parameter.VAR_POSITIONAL: '*',
        inspect.Parameter.VAR_KEYWORD: '**',
    }
    parts = [prefixes.get(arg.kind, ''), arg.name]
    if arg.annotation is not inspect.Parameter.empty:
        annot = arg.annotation
        parts.append(':')
        parts.append(getattr(annot, '__name__', repr(annot)))
    if arg.default is not inspect.Parameter.empty:
        parts.append('=')
        parts.append(repr(arg.default))
    return ''.join(parts)


def signature(f):
    c = Callable(f)
    parts = []
    name = c.code.co_name
    is_lambda = name == '<lambda>'
    if is_lambda:
        parts.append('lambda')
        if c.parameters.values():
            parts.append(' ')
    else:
        parts.append('def ')
        parts.append(name)
        parts.append('(')
    for arg in c.parameters.values():
        parts.append(argument(arg))
        parts.append(', ')
    if c.parameters:
        parts.pop()
    if not is_lambda:
        parts.append(')')
    if 'return' in c.annotations:
        parts.append(' -> ')
        annot = c.annotations['return']
        parts.append(getattr(annot, '__name__', repr(annot)))
    return ''.join(parts)
