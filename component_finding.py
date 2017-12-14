import pickle


class Vertex(object):
    def __init__(self, title, links_to):
        self.index = -1
        self.low_link = -1
        self.on_stack = False

        self.title = title
        self.links_to = links_to
        self.adjacent_nodes = []

    def __repr__(self):
        # return "<Vertex title='%s' index='%i' low_link='%i'>" % (self.title.encode('utf-8'), self.index, self.low_link)
        return "<Vertex '%s'>" % self.title.encode('utf-8')


class Graph(object):
    def __init__(self, graph_dict):
        self.vertices = {title: Vertex(title, links_to) for title, links_to in graph_dict.items()}

        # Now that vertices are in place, make adjacent vertex objects
        # accessible to each vertex.
        for vertex in self.vertices:
            if graph_dict.get(vertex.title):
                for adjacent_title in graph_dict[vertex.title]:
                    vertex.adjacent_nodes.append(self.vertices[adjacent_title])


class Tarjan(object):
    '''
    Adapted from pseudocode found at Wikipedia's article:
    "Tarjan's strongly connected components algorithm"
    https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm
    '''

    def __init__(self, graph):
        self.index = 0
        self.graph = graph
        self.stack = []
        self.strongly_connected_components = []

    def get_components(self):
        for vertex in self.graph.vertices.values():
            if vertex.index == -1:
                self.strong_connect(vertex)
        return self.strongly_connected_components

    def strong_connect(self, v):
        vertex = self.graph.vertices[v.title]

        vertex.index = self.index
        vertex.low_link = self.index

        self.index += 1
        self.stack.append(vertex)
        vertex.on_stack = True

        # Consider successors of v
        for adjacent_title in vertex.links_to:
            adjacent_vertex = self.graph.vertices.get(adjacent_title)
            if adjacent_vertex and adjacent_vertex.index == -1:
                self.strong_connect(adjacent_vertex)
                vertex.low_link = min(vertex.low_link, adjacent_vertex.low_link)
            elif adjacent_vertex and adjacent_vertex.on_stack:
                vertex.low_link = min(vertex.low_link, adjacent_vertex.index)

        # If v is a root node, pop the stack and generate an SCC
        new_strongly_connected_comp = []
        if vertex.low_link == vertex.index:
            adjacent_node = self.stack.pop()
            if adjacent_node.title != vertex.title:
                self.graph.vertices[adjacent_node.title].on_stack = False
                new_strongly_connected_comp.append(adjacent_node)
            while adjacent_node.title != vertex.title:
                adjacent_node = self.stack.pop()
                self.graph.vertices[adjacent_node.title].on_stack = False
                new_strongly_connected_comp.append(adjacent_node)

        if new_strongly_connected_comp:
            self.strongly_connected_components.append(new_strongly_connected_comp)

        return new_strongly_connected_comp


if __name__ == '__main__':
    with open('graph-olin.pickle', 'rb') as f:
        graph_dict = pickle.load(f)

    # Toy graph for testing
    # graph_dict = {
    #     'Cats': ['Meow', 'Kittens', 'Milk'],
    #     'Kittens': ['Dogs'],
    #     'Dogs': ['Cats'],
    #     'Snakes': ['Desert'],
    #     'Desert': ['Snakes'],
    #     'Ice Cream': ['Cones', 'Milk', 'Cows'],
    #     'Cones': ['Flour'],
    #     'Flour': ['Cows'],
    #     'Cows': ['Milk'],
    #     'Milk': ['Ice Cream', 'Cats']
    # }

    graph = Graph(graph_dict)
    tarjan = Tarjan(graph)

    # We know that there will only be one cycle by virtue of our scraping
    sub_cycles = {}
    strongly_connected_components = tarjan.get_components()[0]
    for vertex in strongly_connected_components:
        sub_cycles.setdefault(vertex.low_link, [])
        sub_cycles[vertex.low_link].append(vertex)

    for cycle, vertices in sub_cycles.items():
        print filter(lambda x: x.index == cycle, strongly_connected_components)[0], ':', vertices, '\n'
