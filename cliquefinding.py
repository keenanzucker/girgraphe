import random

class Graph:
    def __init__(self, vertices, adjacency_matrix):
        self.vertices = vertices
        self.adjacency_matrix = adjacency_matrix

def find_adjacent_vertices(vertex, graph):
    vertex_index = -1
    for i in range(len(graph.vertices)):
        if graph.vertices[i] == vertex:
            vertex_index = i
            break
    if vertex_index == -1:
        return []
    adj_mat = graph.adjacency_matrix[vertex_index]
    return [graph.vertices[i] for i in range(len(adj_mat)) if adj_mat[i] == 1]

def intersection(set1, set2):
    set1_dict = {key: True for key in set1}
    set2_dict = {key: True for key in set2}
    intersected = []
    for key, _ in set2_dict.iteritems():
        if key in set1_dict:
            intersected.append(key)
    return intersected

def union(set1, set2):
    union_dict = {key: True for key in set1}
    for element in set2:
        union_dict[element] = True
    return [key for key, _ in union_dict.iteritems()]

def subtract(set1, set2):
    sub_dict = {key: True for key in set1}
    for el in set2:
        _ = sub_dict.pop(el, None)
    return [key for key, _ in sub_dict.iteritems()]

def bron_kerbosch(graph, R, P, X):
    # Base Case
    if len(P) == 0 and len(X) == 0:
        return [R]

    cliques = []

    # Set up pivoting
    pivot_candidates = union(P, X) 
    pivot = pivot_candidates[random.randrange(0, len(pivot_candidates))]
    adj_pivot = find_adjacent_vertices(pivot, graph)
    n_u = subtract(P, adj_pivot)
    for v in n_u:
        # Get new parameters
        adjacent_vertices = find_adjacent_vertices(v, graph)
        newR = union(R, [v])
        newP = intersection(P, adjacent_vertices)
        newX = intersection(X, adjacent_vertices)

        # Run Next Step
        clique_found = bron_kerbosch(graph, newR, newP, newX)
        if len(clique_found) > 0:
            cliques += clique_found

        # Update
        P = subtract(P, [v])
        X = union(X, [v])
    return cliques

if __name__ == '__main__':
    vertices = ["v0", "v1", "v2", "v3"]
    adj_mat = [[0, 1, 0, 0],
                [1, 0, 1, 1],
                [0, 1, 0, 1],
                [0, 1, 1, 0]]
    g = Graph(vertices, adj_mat)
    print bron_kerbosch(g, [], vertices, [])
