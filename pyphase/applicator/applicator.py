__all__ = ['Applicator']

class Applicator:
    @property
    def _iterable(self):
        """Any subclass will need to override this property with
        something that actually returns an iterable
        """
        pass

    def apply(self, func, *args, **kwargs):
        return [func(obj, *args, **kwargs) for obj in self._iterable]

    def aGet(self, attr):
        return self.apply(getattr, attr)

    def aGetFlat(self, attr):
        flat = []
        for sub in self.aGet(attr):
            if sub is not None:
                flat.extend(sub)
        return flat
