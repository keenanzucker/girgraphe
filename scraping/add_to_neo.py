import time
import pickle

from neo4j.v1 import GraphDatabase


class GraphMaker(object):

    def __init__(self, uri, data='data.pickle', graph='graph.pickle'):
        self._driver = GraphDatabase.driver(uri)  # commented out temporarily

        with open('../data/data-olin.pickle', 'rb') as f:
            self.link_to = pickle.load(f)
        with open('../data/graph-olin.pickle', 'rb') as f:
            self.graph = pickle.load(f)

    def start(self):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                for node in self.graph.keys():
                    tx.run('CREATE (start:Article {title: "%s"})' % node)

                for node, items in self.graph.items():
                    for relationship in set.intersection(items, set(self.graph.keys())):
                        if relationship != node:
                            tx.run('MERGE (start:Article {title: "%s"}) \
                                MERGE (target:Article {title: "%s"}) \
                                MERGE (start)-[:LINKS_TO]->(target);' % (node, relationship))

        self.close()

    def purge(self):
        with self._driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run('MATCH (n)-[r]->() DELETE n, r;')
                tx.run('MATCH (n) DELETE n;')

    def close(self):
        self._driver.close()  # Closing neo4j driver


if __name__ == "__main__":
    t = time.time()  # Start time
    maker = GraphMaker('bolt://127.0.0.1:7687')  # URI needed to use neo4j
    maker.start()
    # maker.purge()  # Use this to clear out database
    print time.time() - t  # Total time
