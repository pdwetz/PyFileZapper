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

import datetime
import os
import timeit
import hashlib


class ZapperFile:
    FullPath = ""
    Name = ""
    ContentHash = ""
    Extension = ""
    Directory = ""
    Size = 0
    FileModified = None
    HashTime = 0
    Score = 0

    def __init__(self, directory, name, folderPriority=0):
        self.Directory = directory
        self.Name = name
        self.FullPath = os.path.join(directory, name)
        self.Extension = os.path.splitext(name)[1]
        fileinfo = os.stat(self.FullPath)
        self.FileModified = datetime.datetime.fromtimestamp(fileinfo.st_mtime)
        self.Size = fileinfo.st_size
        self.CalcScore(folderPriority)

    def __getitem__(self, i):
        if i > 10:
            raise IndexError
        return i, 'ZapperFile %d' % i

    def CalcScore(self, folderPriority=0):
        score = folderPriority
        if not ("misc" in self.Directory or "unfiltered" in self.Directory):
            score += 10000
        score += self.Directory.count('\\') * 1000
        score += int((datetime.datetime.now() - self.FileModified).total_seconds() / 31557600)  # seconds in a year
        self.Score = score

    def HashContents(self, blocksize=65536):
        t = timeit.default_timer()
        hasher = hashlib.sha256()
        filecontent = open(self.FullPath, 'rb')
        buf = filecontent.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = filecontent.read(blocksize)
        self.ContentHash = hasher.hexdigest()
        self.HashTime = timeit.default_timer() - t
