import wikipedia
import random

class Vertex:
    def __init__(self, node):
        self.value = node
        self.parent = None

    def set_parent(self, parent):
    	self.parent = parent

    def print_vertex(self):
    	print self.value

    def print_links(self):
    	print get_word_links(self.value)

    def get_vertex_links(self):
    	return get_links(self.value)

    def get_vertex_links_random(self, link_count):
    	return get_random_links(self.value, link_count)

def get_links(word):
	"""if 'ambigous', choose the first one to continue (best guess) or ignore if page not found"""
	try:
		page = wikipedia.page(word)
		return page.links
	except wikipedia.exceptions.DisambiguationError as e:
		try:
			page = wikipedia.page(e.options[0])
			return page.links
		except:
			return []
	except wikipedia.exceptions.PageError:
		print "could not get page for ", word
		return []
	except:
		return []

def get_random_links(word, link_count):
	links = []
	try:
		page = wikipedia.page(word)
		all_links = page.links
		for x in range(link_count):
			links.append(all_links[(random.randrange(0, len(all_links)-1))])

		return links

	except wikipedia.exceptions.DisambiguationError as e:
		try:
			page = wikipedia.page(e.options[0])
			links = page.links
		except:
			return links
	except wikipedia.exceptions.PageError:
		print "could not get page for ", word
		return links
	except:
		return links

def golf(start, searchWord):
	"""Use a BFS to search through wikipedia for search links"""
	queue = []
	path = []
	seen = []
	queue.append({'word': start, 'parent': None})
	seen.append(start)
	levels = 0

	while queue:
		curNode = queue.pop(0)
		print curNode
		vertex = Vertex(curNode['word'])
		vertex.set_parent(curNode['parent'])


		links = vertex.get_vertex_links()
		# links = vertex.get_vertex_links_random(10)

		path.append({'word': vertex.value, 'parent': vertex.parent})
		if links:
			for link in links:
				if link.lower() == searchWord.lower():
					path.append({'word': link, 'parent': vertex.value})
					return find_shortest_path(path)
				else:
					if link not in seen:
						seen.append(link)

						# MODIFIED: To get deeper results faster, only choose 1/20 links
						if random.randrange(0,20) == 0:
							queue.append({'word': link, 'parent': vertex.value})

						# MODIFIED 2: Only add links with fewer letters
						# if len(link) < 10:
						# 	queue.append({'word': link, 'parent': vertex.value})

						# ORIGINAL
						# queue.append({'word': link, 'parent': vertex.value})


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


# sort by smallest number of letters

# Good graph to start: Pkhyan --> Namli Maira --> Abbottabad --> Major James Abbott
startWord = "Giraffe"
searchWord = "Graph"

print golf(startWord, searchWord)






