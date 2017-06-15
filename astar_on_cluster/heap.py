L = 1 << 14
MAX_NODE = L

class Heap:

	def __init__(self):
		self._weight = [float('inf')] * MAX_NODE
		self._count = 0

		''' tree: weight's indices (from 1 to L) '''
		self.tree = [0] * L
		self.tree += [i for i in range(L)]

	def weight(self, p):
		return self._weight[p+1]

	def count(self):
		return self._count

	def empty(self):
		return self._count == 0

	def to_list(self):
		return self._weight[1:]

	def top(self):
		return self.tree[1]-1

	def get(self):
		t = self.top()
		w = self._weight[t+1]
		self.delete(t)
		return t, w
	
	def put(self, p, v):
		if self._weight[p+1] == float('inf'):
			self._count += 1
		if self._weight[p+1] != v:
			self._weight[p+1] = v
			self.update(p+1)

	def update(self, p):
		p += L
		while p > 1:
			p >>= 1
			l = self.tree[p<<1]
			r = self.tree[(p<<1) + 1]

			m = l if self._weight[l] <= self._weight[r] else r
			if self.tree[p] == m:
				if  self._weight[self.tree[p]] \
				 	> self._weight[self.tree[p+(-1 if (p%2) else 1)]]:
					break
			self.tree[p] = m

	def delete(self, p):
		if self._weight[p+1] != float('inf'):
			self._count -= 1
			self._weight[p+1] = float('inf')
			self.tree[L+p+1] = 0
			self.update(p+1)
			#self.update(p)

	def dump(self):
		print self._weight
		#print self.tree
		i = 1
		list = self.tree
		while i <= L:
			print list[L/i:]
			list = list[:L/i]
			i <<= 1

