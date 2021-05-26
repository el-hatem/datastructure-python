class Graph(object):
    def __init__(self, graph={}, gt=True):
        self.graph = graph
        assert isinstance(self.graph, dict)
        self.__is_valid()
        if gt:
            self.__graph_type()
            self.visited = dict()

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

    def degree(self, node):
        result = {}
        for e in self.graph.keys():
            d = self.distance(node, e)

            if node == e:
                result[(node, e)] = 0
            else:
                if d:
                    result[(node, e)] = d
                else:
                    result[(node, e)] = None
        return result

    def __is_valid(self):
        for v in self.graph.values():
            assert isinstance(v, list)

    def __graph_type(self):
        g = self.graph 
        for key in g.keys():
            for v in g[key]:
                if key not in g[v]:
                    self.graph[v].append(key)

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
print(f'{"Graph Details":^50}')
print(f'{"-"*100:^100}')

print("1- ", graph)
print("2-  Graph Length is:", graph.length())
print("5-  Distance between E & A is:", graph.distance("E", "A"))
print("3-  All Paths between E & A:", graph.all_paths("E", "A"))
print("4-  Shortest Path between E & A:", graph.shortest_path("E", "A"))
print("6-  Degree of D: ", graph.degree("D"))
