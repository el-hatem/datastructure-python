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
		if all_paths:
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
		if node in self.get_nodes():
			return True
		else:
			return False

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
			sum_cc = [self.cc(node) for node in self.get_nodes()]
			return sum(sum_cc) / len(sum_cc)

		else:
			if self.is_valid_node(node):
				degree = self.degree(node)
				kv = degree[node]
				nv = 0
				neighbours = self.get_neighbours(node)

				sets_neighbour = []
				for i in range(len(neighbours)):
					for j in range(i+1, len(neighbours)):
						if self.is_connected(neighbours[i], neighbours[j]):
							nv += 1

				return ((2 * nv) / (kv * (kv - 1))) if (kv * (kv - 1)) > 0 else 0.0

				


	def is_connected(self, a, b):
		edges = self.get_edges()
		if (a, b) in edges or (b, a) in edges:
			return True
		return False

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
			standards = ["clique", "star", "grid", "tree", "ring", "chain"]

			nodes = self.get_nodes()

			Graph.rd.shuffle(nodes)

			g = {node: [] for node in nodes}
			if form in standards:
				if form == "clique":
					"""each node is conected to each node"""
					for i in range(len(nodes)-1):
						current_node = nodes[i]
						for j in range(i+1, len(nodes)):
							other_node = nodes[j]
							g[current_node].append(other_node)
							g[other_node].append(current_node)

				elif form == "chain":
					for i in range(len(nodes) - 1):
						g[nodes[i]].append(nodes[i+1])

				elif form == "ring":
					nodes = self.get_nodes()
					for i in range(len(nodes)):
						g[nodes[i]].append(nodes[(i+1)%len(nodes)])

				elif form == "star":
					center_node = nodes.pop(0)
					for i in range(len(nodes)):
						g[center_node].append(nodes[i])
					

				elif form == "tree":
					def make_ranom_tree(nodes, graph={}):
						if len(nodes) == 1:
							return nodes
						make_ranom_tree(nodes[: len(nodes)//2], graph=graph)
						make_ranom_tree(nodes[len(nodes)//2: ], graph=graph)
						right = Graph.rd.choice(nodes[: len(nodes)//2])
						left = Graph.rd.choice(nodes[len(nodes)//2: ]) 
						graph[right].append(left)
						return graph

					g = make_ranom_tree(nodes, g)
					

				elif form == "grid":
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
								g[row_node].append(neighbour_row)
							
							if not (index_i + 1 == i):
								col_node, neighbour_col = grid[index_i][index_j], grid[index_i+1][index_j]
								g[col_node].append(neighbour_col)



			return Graph(g, undirected=self.__undirected)




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
	"A": ["C", "B"],
	"B": ["C", "V"],
	"C": ["V", "G"],
	"D": ["V"],
	"E": ["D", "F"],
	"F": ["V", "G"]
}

graph = Graph(Dict)

clique = graph.transform("clique")
chain = graph.transform("chain")
ring = graph.transform("ring")
grid = graph.transform("grid")
star = graph.transform("star")
tree = graph.transform("tree")
# graph.plot_distribution()
print(graph.cc("V"))
# print(clique.cc("A"))

