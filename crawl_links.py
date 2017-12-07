import time
import pickle

from tqdm import tqdm
import wikipedia


class Crawler(object):

    def __init__(self, uri):
        self.searched = set()
        self.link_to = dict()
        self.graph = dict()

    def get_cached_or_search(self, topic):
        if topic not in self.link_to:
            links = self.get_links(topic)
            self.link_to[topic] = links
        else:
            links = self.link_to[topic]
        return links

    def start(self, starter_topic):
        self.graph[starter_topic] = self.get_links(starter_topic)

        for i, topic in enumerate(self.graph[starter_topic]):
            graph_keys = set(self.graph.keys())
            print 'Searching %s, topic #%i out of %i' % (topic, i, len(self.graph[starter_topic]))

            topic_links = self.get_cached_or_search(topic)

            if set.intersection(graph_keys, topic_links):
                print "Adding %s, %i nodes total \n" % (topic, len(graph_keys) + 1)
                self.graph[topic] = topic_links
                continue
            else:
                print "  |--> Searching %i children of %s" % (len(topic_links), topic)
                for child_topic in tqdm(topic_links):
                    child_topic_links = self.get_cached_or_search(child_topic)

                    if set.intersection(graph_keys, child_topic_links):
                        print "  |--> Found path to items in graph!\n"
                        self.graph[topic] = topic_links
                        self.graph[child_topic] = child_topic_links
                        break

        self.close()

    def get_links(self, topic):
        try:
            links = wikipedia.page(topic).links
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            links = []
            print e
        return set(links)

    def close(self):
        print "Starting pickle process"  # Save data seen so far
        start_time = time.time()

        with open('data-olin.pickle', 'wb') as f:
            pickle.dump(self.link_to, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('graph-olin.pickle', 'wb') as f:
            pickle.dump(self.graph, f, protocol=pickle.HIGHEST_PROTOCOL)

        print "Pickling finished in %f seconds" % (time.time() - start_time)


if __name__ == "__main__":
    t = time.time()  # Start time

    c = Crawler('bolt://127.0.0.1:7687')  # URI needed to use neo4j
    c.start('Franklin W. Olin College of Engineering')

    print time.time() - t  # Total time
