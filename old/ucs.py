import wikipedia

class Graph:
    def __init__(self):
        self.edges = {}
        self.weights = {}

    def neighbors(self, node):
        return self.edges[node]

    def get_cost(self, from_node, to_node):
        return self.weights[(from_node + to_node)]

def search(links, word):
	""" Search through current links """
	for link in links:
		if link.lower() == word.lower():
			print word
			return True

	return False

def golf(start, searchWord):
	""" BFS for wikipedia golf """
	queue = []
	queue.append(start)
	count = 0

	while queue:
		count += 1
		vertex = queue.pop(0)
		print vertex, count
		links = wikipedia.page(vertex).links
		print links
		if search(links, searchWord):
			return True
		else:
			queue = queue + links		

def ucs(graph, start, goal):
    visited = set()
    queue = PriorityQueue()
    queue.put((0, start))

    while queue:
        cost, node = queue.get()
        if node not in visited:
            visited.add(node)

            if node == goal:
                return
            for i in graph.neighbors(node):
                if i not in visited:
                    total_cost = cost + graph.get_cost(node, i)
                    queue.put((total_cost, i))


startWord = "Tardigrade"
searchWord = "Water"
print golf(startWord, searchWord)





