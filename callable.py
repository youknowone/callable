
from __future__ import absolute_import

import sys
import attr

is_py3 = sys.version_info.major >= 3


class temporal_property(object):
    '''Assiginable property'''

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, obj, cls):
        return self.getter(obj)


@attr.s
class Argument(object):
    _prefix = ''
    callable = attr.ib()
    position = attr.ib()
    index = attr.ib()

    @property
    def varname(self):
        return self.callable.code.co_varnames[self.index]

    @property
    def has_default(self):
        raise NotImplementedError

    @property
    def has_annotation(self):
        return self.varname in self.callable.annotations

    @property
    def annotation(self):
        return self.callable.annotations[self.varname]

    @property
    def signature_name(self):
        return self.varname


class PositionalArgument(Argument):

    @property
    def has_default(self):
        boundary = self.callable.code.co_argcount - len(self.callable.defaults)
        return boundary <= self.index

    @property
    def default(self):
        boundary = self.callable.code.co_argcount - len(self.callable.defaults)
        def_idx = self.index - boundary
        return self.callable.defaults[def_idx]


class KeywordOnlyArgument(Argument):
    @property
    def has_default(self):
        return self.varname in self.callable.kwdefaults

    @property
    def default(self):
        return self.callable.kwdefaults[self.varname]


class StarArgument(PositionalArgument):
    _prefix = '*'

    @property
    def has_default(self):
        return False


class DoubleStarArgument(PositionalArgument):
    _prefix = '**'

    @property
    def has_default(self):
        return False


class ArgumentList(list):

    _table = None

    def get(self, varname):
        if self._table is None:
            self._table = {arg.varname: arg for arg in self}
        return self._table[varname]


class Callable(object):

    def __init__(self, f):
        assert callable(f)
        self.callable = f
        self.is_coroutine = getattr(f, '_is_coroutine', None)
        self.decompose()

    def decompose(self):
        self.positional_arguments = ArgumentList()
        self.keyword_only_arguments = ArgumentList()
        self.star_argument = None
        self.double_star_argument = None

        code = self.code

        var_idx = 0
        for var_idx in range(code.co_argcount):
            argument = PositionalArgument(self, var_idx, var_idx)
            self.positional_arguments.append(argument)

        has_sarg = code.co_flags & 4
        pos_sarg = var_idx
        has_ssarg = code.co_flags & 8
        kwonlyargcount = getattr(code, 'co_kwonlyargcount', 0)

        for var_idx in range(var_idx + 1, var_idx + 1 + kwonlyargcount):
            argument = KeywordOnlyArgument(self, bool(has_sarg) + var_idx, var_idx)
            self.keyword_only_arguments.append(argument)

        if has_sarg:
            var_idx += 1
            self.star_argument = StarArgument(self, pos_sarg, var_idx)

        if has_ssarg:
            var_idx += 1
            self.double_star_argument = DoubleStarArgument(self, var_idx, var_idx)

    def iter_arguments(self):
        for arg in self.positional_arguments:
            yield arg
        if self.star_argument:
            yield self.star_argument
        for arg in self.keyword_only_arguments:
            yield arg
        if self.double_star_argument:
            yield self.double_star_argument

    @temporal_property
    def arguments(self):
        arguments = ArgumentList(self.iter_arguments())
        self.arguments = arguments
        return arguments

    @temporal_property
    def code(self):
        '''REAL __code__ for the given callable'''
        c = self.callable
        if self.is_coroutine:
            code = c.__wrapped__.__code__
        else:
            code = c.__code__
        self.code = code
        return code

    @property
    def defaults(self):
        if self.is_coroutine:
            c = self.callable.__wrapped__
        else:
            c = self.callable
        return getattr(c, '__defaults__', None) or ()

    @property
    def kwdefaults(self):
        return getattr(self.callable, '__kwdefaults__', None) or {}

    @property
    def annotations(self):
        return getattr(self.callable, '__annotations__', None) or {}

