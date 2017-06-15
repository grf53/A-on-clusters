from heap import Heap

w_proportional_d = False
distance_max = 10
weight = 10

def get_distance(w):
	return w if w_proportional_d else float(distance_max)/w

def get_path_to(d, pv):
	path = []
	v = d
	while v is not None:
		path.append(v)
		v = pv[v]
	return tuple(reversed(path))

'''
# Name		dijkstra
# Parameter	G: graph which paths are found on
			s: vertex which paths are found from
			d: if it is given, function find path from s to d
# Description
	An implementation of dijkstra algorithm using binary heap.
	The time complexity of this function is O((m+n)log n)
	where n, m are the numbers of vertex and edge each other.
'''
def dijkstra(G, s, d=None):
	visited = []
	visited.append([float('inf')] * len(G))
	visited.append([None] * len(G))
	visited[0][s] = 0
	pv = {}

	q = Heap()
	q.put(s, 0)

	# C = reverse_cluster(v2C, k)
	while not q.empty():
		got = q.get()
		mv = got[0]
		dist = visited[0][mv]
		pv[mv] = visited[1][mv]
		#q.dump()

		if  d == mv:
			return dist, get_path_to(d, pv)

		if visited[0][mv] >= got[1]:
			for v, w in G[mv].items():
				if visited[0][v] > dist+get_distance(w):
					visited[0][v] = dist+get_distance(w)
					visited[1][v] = mv
					q.put(v, visited[0][v])

	return visited[0] if d == None else float('inf')

''' Iterates the function dijkstra() for each node '''
def compute_cluster_heuristics(G):
	H = []
	for v in range(len(G)):
		H.append(weight*dijkstra(G, v))
		#print v, 'done!'

	#for row in H:
	#	print row

	return H

def astar(G, v2C, H, s, d=None):
	''' meta = { open node : [g, pv]} '''
	meta = {}
	''' closed = { node : pv } '''
	closed = {}
	dist = [float('inf')]*len(G)
	dist[s] = 0

	open = Heap()
	open.put(s, H[v2C[s]][v2C[d]])
	meta[s] = (0, None)

	while not open.empty():
		#open.dump()
		''' select the minimum open node '''
		got = open.get()
		mv = got[0]
		g = meta[mv][0]

		''' close the selected '''
		closed[mv] = meta[mv][1]
		#print mv, g
		
		''' Arrived to the destination!!'''
		if mv == d:
			''' return cost and path '''
			return g, get_path_to(d, closed)

		''' for the neighbors of the node mv '''
		for v, w in G[mv].items():
			#print v, w
			#print v2C[v], v2C[d]

			''' calculate new f value '''
			new_f = g + get_distance(w) + H[v2C[v]][v2C[d]]
			#print new_f, g, get_distance(w), H[v2C[v]][v2C[d]]

			''' f for v in queue '''
			m = open.weight(v)

			'''
				open the neighbor unless they are already closed
				or renew it if new f value is less than the elders
			'''
			if v not in closed and m >= new_f:
				open.put(v, new_f)
				meta[v] = [g+get_distance(w), mv]
	
	''' failed to find '''
	return float('inf'), ()
'''
# Name		astar
# Parameter	G	: graph on which the path is found
			v2C	: node-to-cluster mapping table
			H	: pre-calculated cluster heuristics
			s	: the start node of the path to be found 
			d	: the end node of the path to be found
# Return		g	: cost of the found path
			path: found path as the tuple of vertices
# Description
	An implementation of dijkstra algorithm using python PriorityQueue.
	Because python PriorityQueue uses binary heap internally,
	the time complexity of this function is O((m+n)log n)
	where n, m are the numbers of vertex and edge each other.
'''
def astar2(G, v2C, H, s, d):
	'''
	- closed	: python dictionary { closed node : previous node }
		-- (key)    closed node	: a closed(visited in A*) node
		-- (value) previous node	: the node which derives the key
	- q 		: python PriorityQueue [ (f, (mv, pv, g)) ]
		-- (priority) f value	: A* criteria of the open node (f = g + h)
		-- (element)	 tuple	: data for an open node
			--- mv		: index of the open node
			--- pv		: index of the node which derives the mv
			--- g value	: the cost actually paid to reach mv
	'''

	''' Initialization '''
	closed = {}
	q = PriorityQueue()
	q.put((H[v2C[s]][v2C[d]],(s, None, 0)))

	while not q.empty():
		''' select the minimum open node '''
		elmt = q.get()[1]
		mv = elmt[0]
		g = elmt[2]

		''' close the selected '''
		closed[mv] = elmt[1] #pv

		''' Arrived to the destination!!'''
		if mv == d:
			path = []
			v = d
			while v is not None:
				path.append(v)
				v = closed[v]
			path.reverse()

			''' return cost and path '''
			return g, tuple(path)

		''' for the neighbors of the node mv '''
		for v, w in G[mv].items():
			''' calculate new f value '''
			new_f = g + get_distance(w) + H[v2C[v]][v2C[d]]

			''' minimum f for v in queue '''
			#l = [x[0] for x in q.queue if x[1][0] == v]
			#m = min(l) if l else float('inf')

			'''
				open the neighbor unless they are already closed
				or renew it if new f value is less than the elders
			'''
			if v not in closed :#and m >= new_f:
				q.put((new_f, (v, mv, g+get_distance(w))))

	''' failed to find '''
	return float('inf'), ()