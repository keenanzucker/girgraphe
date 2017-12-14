import random, pickle
from neo4j.v1 import GraphDatabase


class Graph(object):
    def __init__(self, uri, data='data.pickle', graph='graph.pickle'):
        self._driver = GraphDatabase.driver(uri, auth=('neo4j', 'password'))  # commented out temporarily

        with open('../data/' + data, 'rb') as f:
            self.link_to = pickle.load(f)
        with open('../data/' + graph, 'rb') as f:
            self.graph = pickle.load(f)

    def vertices(self):
        return self.graph.keys()

    def find_adjacent_vertices(self, vertex):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                links_to = tx.run('MATCH (s: Article)-[:LINKS_TO]->(article: Article {title: "%s"}) RETURN s' % vertex)
                links_from = tx.run('MATCH (s: Article {title: "%s"})-[:LINKS_TO]->(article: Article) RETURN article' % vertex)
        titles_to = [r[0]['title'] for r in links_to.records()]
        titles_from = [r[0]['title'] for r in links_from.records()]
        return intersection(titles_to, titles_from)

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
    adj_pivot = graph.find_adjacent_vertices(pivot)
    n_u = subtract(P, adj_pivot)
    for v in n_u:
        # Get new parameters
        adjacent_vertices = graph.find_adjacent_vertices(v)
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

def create_new_graph(cliques):
    current_letter = 65
    vertices = []
    for c in cliques:
        if len(c) > 1:
            vertices.append((chr(current_letter), c))
            current_letter += 1
    adj_mat = [[0 for i in range(len(vertices))] for i in range(len(vertices))] 
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            weight = len(intersection(vertices[i][1], vertices[j][1]))
            adj_mat[i][j] = weight 
            adj_mat[j][i] = weight 
    return vertices, adj_mat

if __name__ == '__main__':
    g = Graph('bolt://localhost:7687')
    cliques = bron_kerbosch(g, [], g.vertices(), [])
    g = create_new_graph(cliques)
    print g[0] 
    print g[1]
