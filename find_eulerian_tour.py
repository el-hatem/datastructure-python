# Find Eulerian Tour
#
# Write a function that takes in a graph
# represented as a list of tuples
# and return a list of nodes that
# you would follow on an Eulerian Tour
#
# For example, if the input graph was
# [(1, 2), (2, 3), (3, 1)]
# A possible Eulerian tour would be [1, 2, 3, 1]
import random


def degree(tour):
    degree = {}
    for x, y in tour:
        degree[x] = degree.get(x, 0) + 1
        degree[y] = degree.get(y, 0) + 1
    return degree


def is_eularian_circut(graph):
    _degree = degree(graph)
    res = [value % 2 == 0 for value in _degree.values()]
    return (not(False in res))  # or (res.count(False) == 2)


def find_eulerian_tour(graph, current, path=[], stack=[]):
    stack.append(current)
    while stack:
        current = stack[-1]
        check_deg = degree(graph).get(current, 0)
        if check_deg == 0:
            x = stack.pop()
            path.append(x)
        else:
            edge = random.choice([edge for edge in graph if current in edge])
            if current == edge[0]:
                stack.append(edge[1])
            else:
                stack.append(edge[0])
            graph.remove(edge)
    return path


graph = [(1, 2), (2, 4), (3, 4), (1, 3),
         (5, 4), (4, 6), (5, 6), (2, 9), (9, 7), (7, 2)]

if is_eularian_circut(graph):
    node = random.choice(graph)[0]
    print(find_eulerian_tour(graph, node))
