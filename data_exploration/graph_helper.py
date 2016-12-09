import networkx as nx
import math
from collections import Counter
from plotly.graph_objs import *

def build_graph(nodes, edges):
    graph = nx.Graph()
    graph.add_edges_from(edges)
    graph.add_nodes_from(nodes)
    pos=nx.fruchterman_reingold_layout(graph)
    for node in graph.node:
        graph.node[node]['pos'] = pos[node]
    return graph

def build_edge_and_node_trace(node_trace, edge_trace, graph):
    for edge in graph.edges():
        x0, y0 = graph.node[edge[0]]['pos']
        x1, y1 = graph.node[edge[1]]['pos']
        edge_trace['x'] += [x0, x1, None]
        edge_trace['y'] += [y0, y1, None]

    for node in graph.nodes():
        x, y = graph.node[node]['pos']
        node_trace['x'].append(x)
        node_trace['y'].append(y)

    return node_trace, edge_trace


def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)
