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

import os
import timeit
from itertools import groupby
from send2trash import send2trash
from zapperfolder import ZapperFolder
from zapperfile import ZapperFile


def Process():
    processTimer = timeit.default_timer()
    # TODO Setup a config file for initial folder(s) and their respective starting scores
    zfolders = []
    zfolders.append(ZapperFolder(r'F:\test', 100000))
    zfolders.append(ZapperFolder(r'F:\test2', 0))
    zfiles = []
    for zfolder in zfolders:
        for dirname, dirnames, filenames in os.walk(zfolder.FullPath):
            for filename in filenames:
                zfiles.append(ZapperFile(dirname, filename, zfolder.Priority))

    zfiles.sort(key=lambda x: x.Extension + str(x.Size))
    for key, group in groupby(zfiles, lambda x: x.Extension + str(x.Size)):
        grouplist = list(group)
        if len(grouplist) > 1:
            print key + ":  " + str(len(grouplist))
            for f in grouplist:
                f.HashContents()
                print "Size: " + str(f.Size) + " hash time: " + str(f.HashTime)
            grouplist.sort(key=lambda x: x.Score, reverse=True)
            for hashindex, hashgroup in groupby(grouplist, lambda x: x.ContentHash):
                for idx, val in enumerate(hashgroup):
                    if idx == 0:
                        print "Keeping: " + val.FullPath + " (" + str(val.Score) + ")"
                    else:
                        print "Deleting: " + val.FullPath + " (" + str(val.Score) + ")"
                        send2trash(val.FullPath)
        else:
            print "Skipping: " + key

    print '********************'
    print 'Total Files: {:,}'.format(len(zfiles))
    print 'Total Size: {:,}'.format(sum(z.Size for z in zfiles))
    print 'Total Time: {:,}'.format(timeit.default_timer() - processTimer)
    hashed = filter(lambda x: x.ContentHash != '', zfiles)
    print 'Total Hash Files: {:,}'.format(len(hashed))
    print 'Total Hash Size: {:,}'.format(sum(z.Size for z in hashed))
    print 'Total Hash Time: {:,}'.format(sum(z.HashTime for z in hashed))

Process()