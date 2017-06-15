''' return lines read from file '''
def readlines_from_file(filename):
	print 'read: '+filename
	f = open(filename, 'r')
	lines = f.readlines()
	f.close()
	return lines

''' return python premitive variable read from file '''
def read_obj_from_file(filename):
	print 'read: '+filename
	f = open(filename, 'r')
	obj = eval(f.read())
	f.close()
	return obj

''' write python premitive variable to file '''
def write_obj_to_file(filename, obj):
	print 'written: '+filename
	f = open(filename, 'w')
	f.write(str(obj)+'\n')
	f.close()