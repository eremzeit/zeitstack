import sys

total = 0
for arg in sys.argv[1:]:
	total+=len(arg)	
	print '%x, %x' % (total, total & 0xff)
print 'total length: %s, %s' % (str(total), hex(total))
