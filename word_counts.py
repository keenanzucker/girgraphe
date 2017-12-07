import wikipedia
import operator

def search(links, word):
	""" Search through current links """
	for link in links:
		if link.lower() == word.lower():
			print word
			return True
		# else:
		# 	print link + " : " + word

	return False

def golf(start, searchWord):
	""" BFS for wikipedia golf """
	seen = {}
	queue = []
	queue.append(start)
	count = 0

	while queue:
		count += 1
		vertex = queue.pop(0)
		print vertex, count
		links = wikipedia.page(vertex).links
		# print links

		for link in links:

			# add to seen dictionary
			if link in seen:
				seen[link] += 1
			else:
				seen[link] = 1

			# check if word is target word
			if link.lower() == searchWord.lower():
				print searchWord

				# Turn seen dictionary into sorted list of tuples by value
				sortedSeen = sorted(seen.items(), key=operator.itemgetter(1))
				print sortedSeen

				return True

		queue = queue + links		

startWord = "Ceramic"
searchWord = "Water"

#print golf(startWord, searchWord)