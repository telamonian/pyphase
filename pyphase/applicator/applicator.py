from inspect import getfullargspec as getargspec
import numpy as np

__all__ = ['Applicator']

class Applicator:
    @property
    def _iterable(self):
        """Any subclass will need to override this property with
        something that actually returns an iterable
        """
        pass


    def _apply(self, func, *args, **kwargs):
        if 'bcast' in kwargs and kwargs.pop('bcast'):
            return [func(obj, *argGroup, **kwargs)
                    for obj,argGroup in zip(self._iterable, args)] #next(args.__iter__()))]
        else:
            return [func(obj, *args, **kwargs) for obj in self._iterable]

    def _applyMethod(self, meth, *args, **kwargs):
        if 'bcast' in kwargs and kwargs.pop('bcast'):
            return [getattr(obj, meth)(*argGroup, **kwargs)
                    for obj,argGroup in zip(self._iterable, args)] #next(args.__iter__()))]
        else:
            return [getattr(obj, meth)(*args, **kwargs) for obj in self._iterable]

    def _aget(self, attr):
        return [getattr(obj, attr) for obj in self._iterable]


    def _fetch(self, it, flatten=False, array=False):
        if flatten:
            it = self.flatten(it)
        if array:
            it = np.asanyarray(it)

        return it

    def _fetchKwargs(self, kwargs):
        return dict([(k, kwargs.pop(k))
                     for k in getargspec(Applicator._fetch).args[2:]
                     if k in kwargs])

    def apply(self, func, *args, **kwargs):
        fkwargs = self._fetchKwargs(kwargs)
        return self._fetch(self._apply(func, *args, **kwargs), **fkwargs)

    def applyMethod(self, meth, *args, **kwargs):
        fkwargs = self._fetchKwargs(kwargs)
        return self._fetch(self._applyMethod(meth, *args, **kwargs), **fkwargs)

    def aget(self, attr, **kwargs):
        return self._fetch(self._aget(attr), **kwargs)


    @staticmethod
    def flatten(it):
        flat = []
        for sub in it:
            if sub is not None:
                flat.extend(sub)
        return flat
