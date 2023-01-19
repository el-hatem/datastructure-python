from simplemodule import simpleplot


class Graph(object):
	rd = __import__('random')	
	math =  __import__('math')
	def __init__(self, graph={}, undirected=True):
		self.graph = graph
		self.__undirected = undirected

		self.__validate()
		self.__formalize()

	
	def length(self):
		edges = self.get_edges()
		return len(edges)


	def paths(self, start, end, path=[]):
		path = path + [start]
		if start == end:
			return [path]

		paths = []
		for node in self.graph[start]:
			if node not in path:
				paths += self.paths(node, end, path)


		return paths



	def shortest_path(self, start, end):
		all_paths = self.paths(start, end)

		length = float('inf')
		path = None
		
		for p in all_paths:
			path_len = len(p)
			if length > path_len:
				length = path_len
				path = p
		return path



	def distance(self, start, end):
		shortest_path = self.shortest_path(start, end)
		if shortest_path:
			return len(shortest_path) - 1

	def is_valid_node(self, node):
		return True if node in self.get_nodes() else False


	def degree(self, node=None):
		deg = {}

		if not node:
			for e in self.graph.keys():
				deg[e] = len(self.graph[e])
		else:
			if self.is_valid_node(node):
				deg[node] = len(self.graph[node])
		return deg

	def cc(self, node=None):
		if not node:
			ccs = [self.cc(node) for node in self.get_nodes()]
			return sum(ccs) / len(ccs)

		else:
			if self.is_valid_node(node):
				degree = self.degree(node)
				kv = degree[node]
				nv = 0
				neighbours = self.get_neighbours(node)
				edges = self.get_edges()

				for i in range(len(neighbours)):
					for j in range(i+1, len(neighbours)):
						if (neighbours[i], neighbours[j]) in edges or (neighbours[j], neighbours[i]) in edges:
							nv += 1

				return (2 * nv) / (kv * (kv - 1)) if kv > 1 else 0.0

			

	def degree_distribution(self):
		degrees = self.degree()
		distribution = {}
		for node, deg in degrees.items():
			if not r.get(deg, None):
				distribution[deg] = 1
			else:
				distribution[deg] += 1
		return distribution

    # def plot_distribution(self):
    #     datasets = self.degree_distribution()
    #     simpleplot.plot_bars("plot distribution", 600, 600, "degree", "count", [datasets])
    #     simpleplot._block()

	def __validate(self):
		assert isinstance(self.graph, dict)
		for v in self.graph.values():
			assert isinstance(v, list)

	def __formalize(self):
		g = self.graph.copy()
		for node, neighbours in g.items():
			for neighbour in neighbours:
				neigh = self.graph.get(neighbour, [])
				if self.__undirected and node not in neigh:
					neigh += [node]

				self.graph[neighbour] = neigh
				
    
	def transform(self, form="clique"):

			def default_transform(nodes, graph={}):
				return graph

			def clique(nodes, graph={}):
				"""each node is conected to each node"""
				for i in range(len(nodes)-1):
					current_node = nodes[i]
					for j in range(i+1, len(nodes)):
						other_node = nodes[j]
						graph[current_node].append(other_node)
						graph[other_node].append(current_node)
				return graph
			
			def chain(nodes, graph={}):
				"""each node is conected to each node"""
				for i in range(len(nodes) - 1):
					graph[nodes[i]].append(nodes[i+1])
				return graph
			
			def ring(nodes, graph={}):
				"""each node is conected to each node in ring"""
				for i in range(len(nodes)):
					graph[nodes[i]].append(nodes[(i+1)%len(nodes)])
				return graph

			def star(nodes, graph={}):
				"""each node is conected to center node"""
				center_node = nodes.pop(0)
				for i in range(len(nodes)):
					graph[center_node].append(nodes[i])
				return graph

			def grid(nodes, graph={}):
				"""n * m grid format"""
				n = len(nodes)
				p = []
				for i in range(1, n):
					if (n / i) - int(n/i) == 0:
						p.append((i, int(n/i)))

				i, j = Graph.rd.choice(p)
				grid = []
				for index_i in range(i):
					lst = []
					for index_j in range(index_i * j, (index_i * j) + j):
						lst.append(nodes[index_j])
					grid.append(lst)

				for index_i in range(i):
					for index_j in range(j):
						if not (index_j + 1 == j):
							row_node, neighbour_row = grid[index_i][index_j], grid[index_i][index_j+1]
							graph[row_node].append(neighbour_row)
						
						if not (index_i + 1 == i):
							col_node, neighbour_col = grid[index_i][index_j], grid[index_i+1][index_j]
							graph[col_node].append(neighbour_col)
				return graph

			def tree(nodes, graph={}):
				if len(nodes) == 1:
					return nodes
				tree(nodes[: len(nodes)//2], graph=graph)
				tree(nodes[len(nodes)//2: ], graph=graph)

				right = Graph.rd.choice(nodes[: len(nodes)//2])
				left = Graph.rd.choice(nodes[len(nodes)//2: ]) 
				graph[right].append(left)
				return graph

			standards = {
				"clique": clique,
				"star":  star,
				"grid": grid,
				"tree": tree,
				"ring": ring,
				"chain": chain
			}

			nodes = self.get_nodes()
			Graph.rd.shuffle(nodes)
			g = standards.get(form, default_transform)(nodes, graph={node: [] for node in nodes})
			return Graph(g, undirected=self.__undirected)



	def get_tour(self):
	    # your code here
		def check_edge(t, b, nodes):
		    """
		    t: tuple representing an edge
		    b: origin node
		    nodes: set of nodes already visited

		    if we can get to a new node from `b` following `t`
		    then return that node, else return None
		    """
		    if t[0] == b:
		        if t[1] not in nodes:
		            return t[1]
		    elif t[1] == b:
		        if t[0] not in nodes:
		            return t[0]
		    return None

		def connected_nodes(tour):
		    """return the set of nodes reachable from
		    the first node in `tour`"""
		    if len(tour) <= 0:
		    	return tour
		    a = tour[0][0]
		    nodes = set([a])
		    explore = set([a])
		    while len(explore) > 0:
		        # see what other nodes we can reach
		        b = explore.pop()
		        for t in tour:
		            node = check_edge(t, b, nodes)
		            if node is None:
		                continue
		            nodes.add(node)
		            explore.add(node)
		    return nodes

		def generate_eulerian_tour(graph, start=None, tour=[]):

			if not graph:
				return tour + [start]

			edges = [node for node in graph if node[0] == start or node[1] == start]

			g = graph[:]
			edge = None
			while edges:
				edge = edges.pop(0)
				g.remove(edge)
				nodes = self.get_nodes()
				connected = connected_nodes(g)
				if len(nodes) == len(connected):
					break

			x, y = edge
			graph.remove((x, y))
			if (y, x) in graph:
				graph.remove((y, x))
			if x == start:
				tour.append(x)
				start = y
				return generate_eulerian_tour(graph, start=start, tour=tour)
			else:
				tour.append(y)
				start = x
				return generate_eulerian_tour(graph, start=start, tour=tour)


		# main functionality
		degrees = self.degree()
		odd_degree_nodes 	= [v for v, e in degrees.items() if e % 2 == 1]
		even_degree_nodes 	= [v for v, e in degrees.items() if e % 2 == 0 and e != 0]

		if len(odd_degree_nodes) in [0, 2]:
			start = Graph.rd.choice(odd_degree_nodes) if odd_degree_nodes else Graph.rd.choice(even_degree_nodes)
			g = self.get_edges()
			path = generate_eulerian_tour(g, start)
			return path

	
	def get_nodes(self):
		return list(self.graph.keys())


	def get_neighbours(self, node):
		if  self.is_valid_node(node):
			return self.graph[node]
    

	def get_edges(self):
		edges = []
		for node, neighbours in self.graph.items():
			for neighbour in neighbours:
				if not ((node, neighbour) in edges or (neighbour, node) in edges):
					edges.append((node, neighbour))
		return edges

	def insert(self, node, edges=[]):
		assert isinstance(edges, list)
		self.graph[node] = edges
		for node in edges:
			if not self.graph.get(node):
				self.insert(node)
			if self.__undirected:
				self.__formalize()

	def __str__(self):
		return f'Graph: {self.graph}'


Dict = {
	1: [2, 4],
	2: [4,3,5],
	3: [4, 6],
	7: [6, 8]

}

graph = Graph(Dict)

clique = graph.transform("clique")
chain = graph.transform("chain")
ring = graph.transform("ring")
grid = graph.transform("grid")
star = graph.transform("star")
tree = graph.transform("tree")
# graph.plot_distribution()

print(graph.shortest_path(1, 2))
# print(clique.cc("A"))

