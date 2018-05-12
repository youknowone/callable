from __future__ import absolute_import

import sys
from collections import OrderedDict
is_py3 = sys.version_info.major >= 3
if is_py3:
    import inspect
else:
    import inspect2 as inspect
_inspect_iscoroutinefunction = getattr(
    inspect, 'iscoroutinefunction', lambda f: False)

__all__ = ('Callable', )


class temporal_property(object):
    """Assiginable property."""

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter(obj)


class Callable(inspect.Signature):

    def __init__(self, f, *args, **kw):
        s = inspect.signature(f)
        super(Callable, self).__init__(
            s.parameters.values(), return_annotation=s.return_annotation)
        self.callable = f
        self.is_wrapped_coroutine = getattr(f, '_is_coroutine', None)
        self.is_coroutine = self.is_wrapped_coroutine or \
            _inspect_iscoroutinefunction(f)

        self.parameters_values = list(self.parameters.values())

    @temporal_property
    def code(self):
        """REAL __code__ for the given callable."""
        code_owner = self.callable
        if self.is_wrapped_coroutine:
            code_owner = code_owner.__wrapped__
        code = code_owner.__code__
        self.code = code
        return code

    @property
    def annotations(self):
        return getattr(self.callable, '__annotations__', None) or {}

    def kwargify(self, args, kwargs):
        merged = OrderedDict()

        _params = self.parameters_values
        _params_len = len(_params)

        consumed_i = 0
        consumed_names = set()
        i = 0

        # no .POSITIONAL_ONLY support

        while i < _params_len and \
                _params[i].kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            p = _params[i]
            i += 1

            name = p.name
            try:
                value = args[consumed_i]
            except IndexError:
                pass
            else:
                if name in kwargs:
                    raise TypeError(
                        "{}() got multiple values for argument '{}'".format(
                            self.code.co_name, name))
                consumed_i += 1
                merged[name] = value
                continue

            if name in kwargs:
                merged[name] = kwargs[name]
                consumed_names.add(name)
                continue

            value = p.default
            if value is inspect.Parameter.empty:
                message = \
                    "{}() missing required positional argument: '{}'".format(
                        self.code.co_name, p.name)
                raise TypeError(message)
            merged[name] = value

        if i < _params_len and \
                _params[i].kind == inspect.Parameter.VAR_POSITIONAL:
            p = _params[i]
            i += 1

            merged[p.name] = args[consumed_i:]
        else:
            if consumed_i < len(args):
                raise TypeError(
                    "{}() takes {} positional arguments but {} were given"
                    .format(self.code.co_name, i, i + len(args) - consumed_i))

        while i < _params_len and \
                _params[i].kind == inspect.Parameter.KEYWORD_ONLY:
            p = _params[i]
            i += 1

            name = p.name
            if name in kwargs:
                merged[name] = kwargs[name]
                consumed_names.add(name)
            elif p.default is not inspect.Parameter.empty:
                merged[name] = p.default
            else:
                raise TypeError(
                    "{}() missing 1 required keyword-only argument: '{}'"
                    .format(self.code.co_name, p.name))

        var_kws = {k: v for k, v in kwargs.items() if k not in consumed_names}
        if i < _params_len and \
                _params[i].kind == inspect.Parameter.VAR_KEYWORD:
            p = _params[i]
            i += 1

            merged[p.name] = var_kws
        elif var_kws:
            raise TypeError(
                "{}() got multiple values for arguments '{}'".format(
                    self.code.co_name, list(var_kws.keys())))

        return merged
