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

from enum import Enum

class MapFileCell(object):
    """
    Represents a cell in the map grid
    """

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
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def read(self, reader):
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
                for y in range(17):
                    for x in range(17):
                        self._heightmap[(x, y)] = reader.read_float()
                        print('test')
            else:
                raise NotImplementedError('%s is not implemented' % flag)

    def get_world_area_ids(self):
        """
        Returns the cell's areas if present
        """

        contains = self._flags & self.Flags.Area.value
        return self._world_area_ids if contains else []

    def get_terrain_height(self, vector):
        """
        Returns the terrain's height at the supplied vector
        """

        #TODO:

class MapFileGrid(object):
    """
    Represents a grid in the map file
    """

    def __init__(self):
        self._x = 0
        self._y = 0
        self._cells = {}

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def read(self, reader):
        """
        Reads the map grids binary data
        """

        self._x = reader.read_uint()
        self._y = reader.read_uint()

        cell_count = reader.read_uint()
        for i in range(cell_count):
            cell = MapFileCell()
            #cell.read(reader)

            index = (cell.x << 16, cell.y)
            self._cells[index] = cell