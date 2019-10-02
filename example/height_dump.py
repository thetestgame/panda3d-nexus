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

# Set engine configuration
core.load_prc_file_data("example", """
window-title Heightmap Sample
sync-video #f
show-frame-rate-meter #t
""")

class SampleBase(ShowBase):
    """
    Showbase example for Panda3d
    """

    def setup(self):
        """
        Performs setup operations on the showbase
        """

        print('Loading map...')
        self.map_file = nfmap.MapFile.read('example/Arcterra.nfmap')

        for grid_key in self.map_file.grids:
            grid = self.map_file.grids[grid_key]
            print('Processing grid: %s' % grid_key)

            data = []
            px = 0
            print('Reading cells')

            for cell_key in grid.cells:
                cell = grid.cells[cell_key]

                for x in range(17):
                    data.append([])
                    for z in range(17):
                        height = cell.get_terrain_height(core.Vec3(x, 0, z))
                        height = abs(height)
                        height = height / 255
                        data[px].append(height)
                    px += 1

            print('Building image')
            w = len(data)
            h = 17
            print('Size: %s, %s' % (w, h))
            image = core.PNMImage(w, h)
            image.fill(0, 0, 0)

            for x in range(w):
                for y in range(h):
                    v = data[x][y]

                    image.set_red(x, y, v)
                    image.set_green(x, y, v)
                    image.set_blue(x, y, v)

            filepath = core.Filename('output/%s.png' % grid_key)
            image.write(filepath)
            print('Saving: %s ' % filepath.c_str())

        print('Map loaded')

def main():
    """
    Main entry point for the application
    """

    base = SampleBase()
    base.setup()
    base.run()

if __name__ == '__main__':
    sys.exit(main())