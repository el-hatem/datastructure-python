from simplemodule import simplegui
from simplemodule import simpleplot

class Graph(object):
    def __init__(self, graph={}, gt=True):
        self.graph = graph
        self.__type = gt
        assert isinstance(self.graph, dict)
        self.__is_valid()
        if self.__type:
            self.__graph_type()

    def length(self):
        result = set()
        for k, v in self.graph.items():
            for e in v:
                s = tuple(sorted((k, e)))
                result.add((s, ))
        return len(result)

    def _paths(self, start, end, path=[], visit={}):
        path = path + [start]
        if start == end:
            return [path]

        paths = []
        for node in self.graph[start]:
            if node not in path:
                paths += self._paths(node, end, path)

        return paths

    def all_paths(self, start, end):
        return self._paths(start, end)

    def shortest_path(self, start, end):
        paths = self.all_paths(start, end)
        length = float('inf')
        path = None

        if paths:
            for p in paths:
                _len = len(p)
                if length > _len:
                    length = _len
                    path = p
        return path

    def distance(self, start, end):
        result = self.shortest_path(start, end)
        if result:
            return len(result) - 1
        else:
            return None

    def degree(self, node=None):
        result = {}

        if not node:
            for e in self.graph.keys():
                result[e] = len(self.graph[e])
        elif node and node in self.graph.keys():
            result[node] = len(self.graph[node])
        return result

    def degree_distribution(self):
        dist = self.degree()
        r = {}
        print(dist)
        for key, val in dist.items():
            if not r.get(val):
                r[val] = 1
            else:
                r[val] += 1
        return r
    
    def plot_distribution(self):
        datasets = self.degree_distribution()
        print(type(datasets))
        simpleplot.plot_bars("plot distribution", 600, 600, "degree", "count", [datasets])
        simpleplot._block()

    def __is_valid(self):
        for v in self.graph.values():
            assert isinstance(v, list)

    def __graph_type(self):
        g = self.graph
        for key in g.keys():
            for v in g[key]:
                if key not in g[v]:
                    self.graph[v].append(key)

    def insert(self, node, edges=[]):
        assert isinstance(edges, list)
        self.graph[node] = edges
        for node in edges:
            if not self.graph.get(node):
                self.insert(node)
        if self.__type:
            self.__graph_type()

    def __str__(self):
        return f'Graph: {self.graph}'


Dict = {
    "A": ["C", "B", "D"],
    "B": ["E"],
    "C": ["D"],
    "D": ["E"],
    "E": []

}

graph = Graph(Dict)
print(f'{"-"*100:^100}')
print(f'{"Graph Details":^100}')
print(f'{"-"*100:^100}')

print("1- Graph before insertion", graph)

graph.insert("F", ["5", "A"])

graph.plot_distribution()
