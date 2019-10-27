#!/usr/bin/env python
# -*- coding: utf-8 -*-


from collections import Counter


class GameOfLife(object):
    def __init__(self, width=25, height=25, world={}):
        self.start = 0
        self.width = width
        self.height = height
        self.world = world

        if not self.world:
            self.create_world()

    def create_world(self):
        self.world = {(3, 1), (1, 2), (1, 3), (2, 3)}

    def change_world(self, world):
        self.world = world

    def get_neighbors(self, cell):
        (x, y) = cell
        return [(x-1, y-1), (x, y-1), (x+1, y-1),
                (x-1, y),             (x+1, y),
                (x-1, y+1), (x, y+1), (x+1, y+1)]

    def get_neighbor_counts(self, world):
        return Counter(nb for cell in world for nb in self.get_neighbors(cell))

    def next_generation(self):
        possible_cells = counts = self.get_neighbor_counts(self.world)
        return {cell for cell in possible_cells
                if (counts[cell] == 3)
                or (counts[cell] == 2 and cell in self.world)}

    def run(self, n):
        for g in range(n):
            print("Gen {}".format(g))
            self.world = self.next_generation()
        return self.world


if __name__ == "__main__":
    app = GameOfLife()
    print(app.run(3))
