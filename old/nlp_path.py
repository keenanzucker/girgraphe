from nltk.corpus import wordnet

# dog = wn.synset('dog.n.01')

# print dog.path_similarity(cat)

w1 = wordnet.synset('bread.n.01')
w2 = wordnet.synset('bagel.n.01')

print(w1.wup_similarity(w2))