import sys
from random import randrange

import distances
from algorithms import compute_cluster_heuristics
from io import readlines_from_file, write_obj_to_file

''' if a and b are given, it makes the graph weighted '''
def refine_graph(lines, a=None, b=None):
	head_words = lines[0].split()
	G = []

	weighted = False
	if len(head_words) == 3 and head_words[2] == '1':
		weighted = True
	for i, l in enumerate(lines[1:]):
		G.append({})
		words = l.split()
		if weighted:
			iwords = iter(words)
			for e, w in zip(iwords, iwords):
				G[i][int(e)-1] = int(w)
		else:
			for e in words:
				G[i][int(e)-1] = 1 if (a == None or b == None) \
								else randrange(a, b)

	return G

def refine_cluster(lines):
	return map(int, lines)

'''
# NOT USED
def reverse_cluster(v2C, k):
	C = []

	for i in range(k):
		C.append([])
	for i, c in enumerate(v2C):
		C[c].append(i)
	return C
'''

def make_graph_with_cluster(G, v2C, k):
	'''
		- f_distance	: python dictionary { method : function }
		- usage		: f_distance[<method>](list)
			-- method	: method how to calculate distance
			-- list		: list of the weights
		- description :
			functions which return distances for the given weight list
	'''
	f_distance = {'min': min,
			'unit_hmean': distances.harmonic_mean_unit,
			'hmean': distances.harmonic_mean,
			'amean': distances.arithmetic_mean}
	D = []
	bridges = {}
	for i in range(k):
		D.append({})

	'''
		time complexity of following code is O(|E|)
									where E is the edge set of graph.
		c.f.) if edges are undirected, the complexity becomes O(2|E|).
	'''
	for v1, d1 in enumerate(G):
		for v2 in d1.keys():
			C1 = v2C[v1]
			C2 = v2C[v2]
			if C1 != C2:
				if (C1, C2) not in bridges:				
					bridges[(C1, C2)] = [d1[v2]]
				else:
					bridges[(C1, C2)].append(d1[v2])

	for (C1, C2), list in bridges.items():
		D[C1][C2] = f_distance['unit_hmean'](list)
		#D[C1][C2] = f_distance['min'](list)

	return D

def main():
	if len(sys.argv) != 3:
		print "usage: $ python {} <graph file> <cluster file>"\
							.format(sys.argv[0])
		return

 	''' the number of the clusters '''
	k = eval(sys.argv[2].split('.')[-1])

	''' graph refined as a python variable from the graph file '''
	G = refine_graph(readlines_from_file(sys.argv[1]), 1, 500)

	''' v2C	: node-to-cluster mapping table '''
	v2C = refine_cluster(readlines_from_file(sys.argv[2]))
	# ''' C	: cluster-to-nodes mapping table (NOT USED)'''
	# C = reverse_cluster(v2C, k)

	''' graph of which nodes are clusters '''
	D = make_graph_with_cluster(G, v2C, k)
	
	''' write the pre-processed data as files '''
	compute_cluster_heuristics(G)
	write_obj_to_file(sys.argv[1].split('/')[1]+'.part.refine', v2C)
	write_obj_to_file(sys.argv[1].split('/')[1]+'.refine', G)
	write_obj_to_file(sys.argv[1].split('/')[1]+'.heuristics', 
						compute_cluster_heuristics(D))


if __name__ == '__main__':
	main()

