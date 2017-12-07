import wikipedia

class Vertex:
    def __init__(self, node):
        self.value = node
        self.parent = None

    def set_parent(self, parent):
    	self.parent = parent

    def print_vertex(self):
    	print self.value

    def print_links(self):
    	print getLinks(self.value)

    def get_links(self):
    	return getLinks(self.value)

def getLinks(word):
	"""if 'ambigous', choose the first one to continue (best guess) or ignore if page not found"""
	try:
		page = wikipedia.page(word)
		return page.links
	except wikipedia.exceptions.DisambiguationError as e:
		page = wikipedia.page(e.options[0])
		return page.links
	except wikipedia.exceptions.PageError:
		print "could not get page for ", word
		return []
	except:
		return []

def golf(start, searchWord):
	"""Use a BFS to search through wikipedia for search links"""
	queue = []
	path = []
	queue.append({'word': start, 'parent': None})
	levels = 0

	while queue:
		curNode = queue.pop(0)
		vertex = Vertex(curNode['word'])
		vertex.set_parent(curNode['parent'])
		links = vertex.get_links()
		path.append({'word': vertex.value, 'parent': vertex.parent})

		for link in links:
			if link.lower() == searchWord.lower():
				path.append({'word': link, 'parent': vertex.value})
				return find_shortest_path(path)
			else:
				queue.append({'word': link, 'parent': vertex.value})
		

def find_shortest_path(path):
	"""Using all of the links in the path, filter backwards using the parents to return the correct path"""
	shortest_path = []
	path = path[::-1]
	final = path[-1]
	node = path[0]

	while node != final:
		shortest_path.append(node['word'])
		for link in path:
			if node['parent'] == link['word']:
				shortest_path.append(link['word'])
				node = link

	return " --> ".join(shortest_path[::-1])


startWord = "Pkhyan"
searchWord = "Major James Abbott"

print golf(startWord, searchWord)






