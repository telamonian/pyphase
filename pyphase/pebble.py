from copy import copy as shallowcopy

__all__ = ['Pebble']

class Pebble:
    def __init__(self, land, history=None):
        self.land = land
        self.history = [] if history is None else shallowcopy(history)

    def setLand(self, land):
        self.history.append(self.land)
        self.land = land

    def copy(self):
        return Pebble(self.land, self.history)

    def fail(self):
        self.setLand(None)

    def revive(self, land):
        if self.land is None:
            self.land = land
        else:
            self.setLand(land)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.land.__str__()
