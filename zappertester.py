'''
    PyFileZapper - Finds and removed duplicate files
    Copyright (C) 2013 Peter Wetzel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
__author__ = 'Peter Wetzel'

import unittest
import os
from zapperfile import ZapperFile


class ZapperTester(unittest.TestCase):
    FillerText = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n";

    def test_zapperfile_load(self):
        filename = "test_zapperfile_load.txt"
        self.CreateFile(filename)
        zfile = ZapperFile(".", filename)
        self.assertEqual(zfile.Name, filename)
        self.assertEqual(zfile.Extension, ".txt")
        self.assertGreater(zfile.Size, 0)
        self.assertGreater(zfile.Score, 0)
        self.assertIsNotNone(zfile.FileModified)
        os.remove(filename)

    def test_zapperfile_hash(self):
        filename = "test_zapperfile_hash.txt"
        self.CreateFile(filename)
        zfile = ZapperFile(".", filename)
        zfile.HashContents()
        self.assertIsNot(zfile.ContentHash, "")
        os.remove(filename)

    def CreateFile(self, filename, fillerlines=1):
        f = open(filename, "w")
        for filler in range(fillerlines):
            f.write(self.FillerText)
        f.close()

if __name__ == '__main__':
    unittest.main()
