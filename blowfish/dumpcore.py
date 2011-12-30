import os
import sys
import string


#
# find the latest core dump
#
paths = os.listdir('.')
paths = filter(lambda x: string.find(x, 'core') == 0, paths)

max_time = -1
max_time_path = None
for path in paths:
    mtime = os.lstat('./' + path).st_mtime
    if mtime > max_time:
        max_time = mtime
        max_time_path = path

fname = 'dumpmemory.gdb__109850978258'
print 'using  --> %s' % max_time_path
os.system('echo dump memory ./smemory 0xbfff0000 0xbfffe100 > ' + fname)
os.system('echo dump memory ./cmemory 0x08040000 0x0804ffff >> ' + fname)
os.system('gdb -batch -c %s -x %s' % (max_time_path, fname))
os.system('rm %s' % fname)
os.system('hd smemory')
os.system('hd cmemory')

