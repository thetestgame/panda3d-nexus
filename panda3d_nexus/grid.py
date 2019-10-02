"""
MIT License

Copyright (c) 2019 Jordan Maxwell
Written 10/02/2019

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from panda3d import core

from direct.directnotify.DirectNotifyGlobal import directNotify

from enum import Enum
import math

from . import reader, constants

class MapFileCell(object):
    """
    Represents a cell in the map grid
    """

    notify = directNotify.newCategory('cell')
    notify.setDebug(True)

    class Flags(Enum):
        Empty = 0
        Area = 1
        Height = 2
        Aura = 4
        Liquid = 8

    def __init__(self):
        self._x = 0
        self._y = 0 
        self._flags = 0

        self._world_area_ids = {}
        self._heightmap = {}

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def heightmap(self):
        return self._heightmap

    def read(self, reader: reader.BinaryReader):
        """
        Reads the cells binary data
        """

        self._x = reader.read_uint()
        self._y = reader.read_uint()

        self._flags = reader.read_uint()

        for i in range(32):
            flag = 1 << i

            if (self._flags & flag) == 0:
                continue

            if flag == self.Flags.Area.value:
                for j in range(4):
                    self._world_area_ids[j] = reader.read_uint()
            elif flag == self.Flags.Height.value:
                for x in range(17):
                    for y in range(17):
                        self._heightmap[(x, y)] = reader.read_float()
            else:
                self.notify.error('%s is not implemented' % flag)

        if self.notify.getDebug():
            self.notify.debug('Loaded %s areas' % len(self._world_area_ids))
            self.notify.debug('Loaded %s heightmap points' % len(self._heightmap))

    def get_world_area_ids(self) -> list:
        """
        Returns the cell's areas if present
        """

        contains = self._flags & self.Flags.Area.value
        return self._world_area_ids if contains else []

    def get_terrain_height(self, vector: core.Vec3) -> float:
        """
        Returns the terrain's height at the supplied vector
        """

        # Verify heightmap data is present
        if not len(self._heightmap):
            self.notify.warning('Attempting to retrieve from an empty cell')
            return 0

        true_x = vector.get_x() + constants.world_grid_origin * constants.grid_size
        true_z = vector.get_z() + constants.world_grid_origin * constants.grid_size

        vertex_x = int(math.floor(true_x / 2.0))
        local_vertex_x = vertex_x & 15
        vertex_y = int(math.floor(true_z / 2.0))
        local_vertex_y = vertex_y & 15

        p1 = self._heightmap[(local_vertex_x + 1, local_vertex_y)]
        p2 = self._heightmap[(local_vertex_x, local_vertex_y + 1)]

        sq_x = (true_x / 2) - vertex_x
        sq_z = (true_z / 2) - vertex_y

        height = 0
        if (sq_x + sq_z) < 1:
            p0 = self._heightmap[(local_vertex_x, local_vertex_y)]
            height = p0
            height += (p1 - p0) * sq_x
            height += (p2 - p0) * sq_z
        else:
            p3 = self._heightmap[(local_vertex_x + 1, local_vertex_y + 1)]
            height = p3
            height += (p1 - p3) * (1.0 - sq_z)
            height += (p2 - p3) * (1.0 - sq_x)

        return height

class MapFileGrid(object):
    """
    Represents a grid in the map file
    """

    notify = directNotify.newCategory('grid')

    def __init__(self):
        self._x = 0
        self._y = 0
        self._cells = {}

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def cells(self) -> dict:
        return self._cells

    def read(self, reader: reader.BinaryReader):
        """
        Reads the map grids binary data
        """

        self._x = reader.read_uint()
        self._y = reader.read_uint()

        cell_count = reader.read_uint()
        for i in range(cell_count):
            cell = MapFileCell()
            cell.read(reader)

            index = (cell.x << 16, cell.y)
            self._cells[index] = cell

        if self.notify.getDebug():
            self.notify.debug('Loaded %s cells' % len(self._cells))