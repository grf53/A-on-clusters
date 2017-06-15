from datetime import datetime
from random import randrange
import sys

from algorithms import dijkstra, astar
from io import read_obj_from_file

def main():
	if len(sys.argv) != 4:
		print "usage: $ python {} <refined graph file> <refined cluster file> <heuristics file>".format(sys.argv[0])
		return

	G = read_obj_from_file(sys.argv[1])
	v2C = read_obj_from_file(sys.argv[2])
	H = read_obj_from_file(sys.argv[3])

	print "Put node as integer for each."
	print "(0 - {}; negative to terminate)".format(len(G)-1)
	#while 1:
	f = open('add32.data', 'w')
	for i in range(10000):
		#src = input("Source Node >> ")
		#dest = input("Destination Node >> ")

		src = randrange(len(G))
		dest = randrange(len(G))
		while src == dest:
			dest = randrange(len(G))

		if src < 0 or dest < 0:
			print "negative input: Terminate"
			break
		elif src > len(G) or dest > len(G):
			print "input out of range"
			continue
		elif src == dest:
			print 0
			continue
		
		t1 = datetime.now()
		ddistance, dpath = dijkstra(G, src, dest)
		t2 = datetime.now()
		adistance, apath = astar(G, v2C, H, src, dest)
		t3 = datetime.now()
	
		f.write('{}\t{}\n'.format((adistance/ddistance), \
					(float((t2-t1).microseconds)/(t3-t2).microseconds)))

		#print '{:>8}:'.format('dijkstra'), ddistance, dpath, t2-t1
		#print '{:>8}:'.format('a*'), adistance, apath, t3-t2
	f.close()

if __name__ == '__main__':
	main()