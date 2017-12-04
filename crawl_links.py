import time
import pickle

from tqdm import tqdm
import wikipedia
from neo4j.v1 import GraphDatabase


class Crawler(object):

    def __init__(self, uri):
        # self._driver = GraphDatabase.driver(uri)  # commented out temporarily
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

        # Different version of scraper, keeping for one commit for reference.
        # while len(self.graph.keys()) < 200:
        #     topic = self.queue.pop()
        #     if topic in self.searched:
        #         print "\n\n!*!*!*!* Already searched %s \n\n" % topic
        #         continue

        #     new_links = self.get_links(topic)
        #     self.link_to[topic] = new_links
        #     if set.intersection(new_links, self.graph.keys()):
        #         self.graph[topic] = new_links
        #         self.queue
        #     self.queue.update(new_links)
        #     self.queue -= self.searched
        #     self.searched.add(topic)

        #     print "Topic: %s, searched so far: %s, links: %i" % (
        #         topic, len(self.searched), len(self.queue)
        #     )

        self.close()

    def get_links(self, topic):
        try:
            links = wikipedia.page(topic).links
        except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
            links = []
            print e

        # neo4j command to get Article node and build relevant connections,
        # temporarily commented but leaving as reference.
        # with self._driver.session() as session:
        #     with session.begin_transaction() as tx:
        #         for link in links:
        #             tx.run('MERGE (start:Article {title: "%s"}) \
        #                 MERGE (target:Article {title: "%s"}) \
        #                 MERGE (start)-[:LIKES]->(target);' % (topic, link))

        return set(links)

    def close(self):
        print "Starting pickle process"  # Save data seen so far
        start_time = time.time()

        with open('data.pickle', 'wb') as f:
            pickle.dump(self.link_to, f, protocol=pickle.HIGHEST_PROTOCOL)

        with open('graph.pickle', 'wb') as f:
            pickle.dump(self.graph, f, protocol=pickle.HIGHEST_PROTOCOL)

        print "Pickling finished in %f seconds" % (time.time() - start_time)


if __name__ == "__main__":
    t = time.time()  # Start time

    c = Crawler('bolt://127.0.0.1:7687')  # URI needed to use neo4j
    c.start('Kellia')

    print time.time() - t  # Total time
