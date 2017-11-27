import wikipedia
import random

tart = wikipedia.page("Tardigrade")


def search(links, word):
	for link in links:
		if link.lower() == word.lower():
			print word
			return True
		# else:
		# 	print link + " : " + word

	return False

def golf(start, searchWord):
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

		#print queue
		

searchWord = "Water"
print golf("Tardigrade", searchWord)