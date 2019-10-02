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
from direct.stdpy.file import *

from . import reader, grid, constants

import math

class MapFile(object):
    """
    Represents a NFMap file
    """

    notify = directNotify.newCategory('map')
    notify.setInfo(True)

    MAGIC = 1347241550
    VERSION = 2
    BUILD = 16042

    def __init__(self):
        self._asset = None
        self._grids = {}

    @property
    def asset(self) -> str:
        return self._asset

    @property
    def grids(self) -> dict:
        return self._grids

    @classmethod
    def read(cls, filepath: str):
        """
        Reads the map file from disk
        """

        map_file = cls()
        map_file.notify.info('Reading map file: %s' % filepath)
        with open(filepath, 'rb') as f:
            bin_reader = reader.BinaryReader(f)
            map_file.parse(bin_reader)

        return map_file

    def parse(self, reader: reader.BinaryReader):
        """
        Parses the data contained in the map file
        """

        self.__read_header(reader)
        self._asset = reader.read_string()
        
        grid_count = reader.read_uint()
        for grid_index in range(grid_count):
            file_grid = grid.MapFileGrid()
            file_grid.read(reader)

            index = file_grid.x << 16 | file_grid.y
            if index in self._grids:
                raise ValueError('Index already exists: %s' % index)
            
            self._grids[index] = file_grid

    def __read_header(self, reader: reader.BinaryReader):
        """
        Reads the map file header
        """

        magic = reader.read_uint() 
        version = reader.read_uint()
        build = reader.read_uint()

        assert magic == self.MAGIC
        assert version == self.VERSION
        assert build == self.BUILD

    def get_world_area_id(self, vector: core.Vec2) -> int:
        """
        Return world area id at the supplied position
        """

        grid = self.get_grid(vector)
        if not grid:
            return 0

        return grid.get_world_area_id(vector)

    def get_terrain_height(self, vector: core.Vec2) -> float:
        """
        Returns the terrain height at the supplied position
        """

        grid = self.get_grid(vector)
        if not grid:
            return 0

        return grid.get_terrain_height(vector)

    def get_grid(self, vector: core.Vec2) -> grid.MapFileGrid:
        """
        Returns the grid at the given position
        """

        gridx, gridy = self.__get_grid_coord(vector)
        index = gridy << 16 | gridx
        return self._grids.get(index, None)

    def get_grid_exact(self, vector: core.Vec2) -> grid.MapFileGrid:
        """
        Returns the grid at the exact grid coordinate specified
        """

        index = int(vector.get_y()) << 16 | int(vector.get_x())
        return self._grids.get(index, None)        

    def __get_grid_coord(self, vector: core.Vec2) -> (float, float):
        """
        Returns the grid coordinate from the Vec3 position
        """

        x = int(math.floor(
            constants.grid_cell_count * constants.world_grid_origin + vector.get_x() / constants.grid_size))

        if x < 0 or x > constants.world_grid_count * constants.grid_cell_count:
            self.notify.error('Position X: %s is invalid' % x)

        y = int(math.floor(
            constants.grid_cell_count * constants.world_grid_origin + vector.get_y() / constants.grid_size))
        if y < 0 or y > constants.world_grid_count * constants.grid_cell_count:
            self.notify.error('Position Y: %s is invalid' % y)

        return (x, y)