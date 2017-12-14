import wikipedia
import sys
import pickle


class Vertex:
    def __init__(self, node):
        self.value = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited        
        self.visited = False  
        self.neighbors = wikipedia.page(node).links

    def print_vertex(self):
    	print self.value

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_visited(self):
        self.visited = True

class Graph:
	def __init__(self):
		self.vertices = [];

	def add_vertex(self, vertex):
		self.vertices.append(vertex)

	def print_graph(self):
		for vertex in self.vertices:
			vertex.print_vertex()	


if __name__ == '__main__':
	# startWord = "Neil Young"
	# searchWord = "United States"
	# v = Vertex(startWord)

	# g = Graph()
	# g.add_vertex(v)

	# for edge in v.neighbors:
	# 	v_new = Vertex(edge)
	# 	g.add_vertex(v_new)

	# g.print_graph()


	# with open('data.pickle', 'rb') as f:
	# 	link = pickle.load(f)
	with open('graph.pickle', 'rb') as f:
		graph = pickle.load(f)

	#print golf(startWord, searchWord)

	# print link
	print graph










