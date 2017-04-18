
from callable import Callable


def argument(arg):
    parts = [arg._prefix, arg.varname]
    if arg.has_annotation:
        annot = arg.annotation
        parts.append(':')
        parts.append(getattr(annot, '__name__', repr(annot)))
    if arg.has_default:
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
        if c.arguments:
            parts.append(' ')
    else:
        parts.append('def ')
        parts.append(name)
        parts.append('(')
    for arg in c.arguments:
        parts.append(argument(arg))
        parts.append(', ')
    if c.arguments:
        parts.pop()
    if not is_lambda:
        parts.append(')')
    if 'return' in c.annotations:
        parts.append(' -> ')
        annot = c.annotations['return']
        parts.append(getattr(annot, '__name__', repr(annot)))
    return ''.join(parts)
