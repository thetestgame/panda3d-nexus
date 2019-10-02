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

import sys

from panda3d import core

from direct.showbase.ShowBase import ShowBase

from panda3d_nexus import map as nfmap

class SampleBase(ShowBase):
    """
    Showbase example for Panda3d
    """

    def setup(self):
        """
        Performs setup operations on the showbase
        """

        self.map_file = nfmap.MapFile.read('example/Arcterra.nfmap')
        grid_pos = core.Vec2(58, 58)
        grid = self.map_file.get_grid_exact(grid_pos)

        for cell_key in grid.cells:
            cell = grid.cells[cell_key]
            heightpoints = cell.heightmap

            for point_key in heightpoints:
                point = heightpoints[point_key]

def main():
    """
    Main entry point for the application
    """

    base = SampleBase()
    base.setup()
    base.run()

if __name__ == '__main__':
    sys.exit(main())