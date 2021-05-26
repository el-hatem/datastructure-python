class Graph(object):
    def __init__(self, graph={}):
        self.graph = graph
        assert isinstance(self.graph, dict)
        self.is_valid()

    def length(self):
        result = set()
        for k, v in self.graph.items():
            for e in v:
                s = tuple(sorted((k, e)))
                result.add((s, ))
        return len(result)

    def all_paths(self, start, end, path=[]):
        if not(start in self.graph.keys() and end in self.graph.keys()):
            return None

        path = path + [start]
        if end in self.graph[start] or start in self.graph[end]:
            return [path+[end]]
        else:
            paths = []
            for node in self.graph[start]:
                paths += self.all_paths(node, end, path)
            return paths

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
            d = self.distance(e, node)

            if node == e:
                result[(node, e)] = 0
            else:
                if d:
                    result[(node, e)] = d
                else:
                    result[(node, e)] = None
        return result

    def is_valid(self):
        for v in self.graph.values():
            assert isinstance(v, list)

    def __str__(self):
        return f'Graph: {self.graph}'


Dict = {
    "1": ["2", "3"],
    "2": ["3"],
    "3": ["4"],
    "4": [],
    "5": []
}

graph = Graph(Dict)
print("All Paths between '1' & '4': ", graph.all_paths("1", "4"))
print("Shortest Path between '1' & '4': ", graph.shortest_path("1", "4"))
print("Distance between '1' & '4': ", graph.distance("1", "4"))
print("Degree of '4' with other nodes: ", graph.degree("4"))
