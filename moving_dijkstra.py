# -*- coding: utf-8 -*-

import sys
import wikipedia
from collections import deque

def process_topic(distances, next_topics, topic):
    ''' Distances is a hash table, mapping destination to origins, next_topics is a queue of topics, topic is the current topic '''
    links = get_links(topic)
    for link in links:
        next_topics.append(link)
        distances = update_distances(distances, (topic, link))
    return distances, next_topics

def update_distances(distances, edge):
    ''' Distances is a hash table, mapping destination to origins, edge is tuple with the form (origin, destination) Running Time: O(n)'''
    # update the edge to be 1
    origin = edge[0]
    destination = edge[1]
    dist_dest = distances.get(destination, {})
    dist_dest[origin] = 1
    distances[destination] = dist_dest

    # update for all keys
    for dest, origins in distances.iteritems():
        if dest != destination and origin in origins:
            # Similar to Dijkstra, if the link does not exists, it is infinite
            current_distance = distances[destination].get(dest, sys.maxint)
            updated_distance = min(current_distance, origins[origin] + 1)
            distances[destination][dest] = updated_distance
    return distances

def get_links(topic):
    try:
        links = wikipedia.page(topic).links
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError) as e:
        links = []
    return links

if __name__ == "__main__":
    d = deque()
    d.append('New Orleans, Louisiana')
    distances = {}

    count = 0
    while len(d) != 0 and count < 10:
        count += 1
        topic = d.popleft()
        print topic
        distances, d = process_topic(distances, d, topic)

    print distances['11th Ward of New Orleans']['12 Years a Slave (film)']
