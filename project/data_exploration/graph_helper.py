import networkx as nx
import math
from collections import Counter
from ast import literal_eval
from plotly.graph_objs import *


def build_graph(nodes, edges, coordinate=True, weighted_edge=False):
    graph = nx.Graph()
    if weighted_edge:
        graph.add_weighted_edges_from(edges)
    else:
        graph.add_edges_from(edges)
    graph.add_nodes_from(nodes)
    if coordinate:
        pos=nx.fruchterman_reingold_layout(graph)
        for node in graph.node:
            graph.node[node]['pos'] = pos[node]
    return graph


def build_edge_and_node_trace(n_trace, e_trace, graph):
    node_trace = n_trace
    edge_trace = e_trace
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
    maga = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magb = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (maga * magb)


def clean_score(list_of_score, origin):
    raw_score = [int(score['score']) for score in list_of_score if int(score['postId']) == origin]
    score_cleaned = filter(lambda not_take: not_take != -1, raw_score)
    return filter(lambda empty: empty is not None, score_cleaned)


def get_students_data(students, origin, destination=None):
    students_with_both_videos = []
    for student in students:
        chosen_video = student['chosenVideo']
        if destination:
            if all(video in chosen_video for video in [origin, destination]):
                if chosen_video.index(origin) == chosen_video.index(destination) - 1:
                    student_target = dict([('student_id', student['memberId'])])
                    student_target['score'] = clean_score(student['listenScore'], origin)
                    students_with_both_videos.append(student_target)
        else:
            if origin in chosen_video:
                student_target = dict([('student_id', student['memberId'])])
                student_target['score'] = clean_score(student['listenScore'], origin)
                students_with_both_videos.append(student_target)
    return students_with_both_videos


# Return a tuple (score_values, frequencies) sorted by values
def get_distibution_sorted(students_data):
    score_frequency = []
    for student in students_data:
        for score in student['score']:
            if score in score_frequency:
                score_frequency[score] += 1
            else:
                score_frequency[score] = 1
    score_frequency_sorted = sorted(score_frequency, key=lambda student_score: student_score[0])
    return [couple[0] for couple in score_frequency_sorted], [couple[1] for couple in score_frequency_sorted]


# Take a graph and a node in input and return a list of tuple (neighboor, weight) sorted by weight
def get_neighboors_weighted_sorted_by_weight(graph, node):
    neighboors = list(reversed(sorted(graph[node].items(), key=lambda edge: edge[1]['weight'])))
    neighboors = [(neighboor[0], neighboor[1]['weight']) for neighboor in neighboors]
    return neighboors


# Take in input a tuple (neighboor, weight) and return the main neighboors based on pareto ratio
def select_main_neighboors(neighboors_weighted, treeshold=0.8):
    users = sum([neighboor[1] for neighboor in neighboors_weighted])
    users_to_keep = users * treeshold
    print users_to_keep
    user_counter = 0.0
    node_nb = 0
    while user_counter <= users_to_keep:
        user_counter += neighboors_weighted[node_nb][1]
        node_nb += 1
    return neighboors_weighted[:node_nb - 1]


# Take the graph in input and return a list of tuple (node, ratio) sorted by ratio
def get_indegree_outdegree_ratio(graph, origin):
    nodes = []
    for node in graph.nodes():
        if node != origin:
            in_degree = graph.in_degree(node, weight="weight")
            out_degree = graph.out_degree(node, weight="weight")
            stop_percentage = out_degree / float(in_degree)
            nodes.append((node, stop_percentage))
    return list(reversed(sorted(nodes, key=lambda video: video[1])))


def building_directed_weighted_grah(students):
    graph = nx.DiGraph()
    edges = []
    for student in students:
        videos = student['chosenVideo']
        if videos > 1:
            user_path = []
            for index, video in enumerate(videos):
                if index != (len(videos) - 1):
                    user_path.append((videos[index], videos[index + 1]))
            edges += user_path

    frequency_edge = {}
    for edge in edges:
        edge_string = str(edge)
        if edge_string in frequency_edge:
            frequency_edge[edge_string] += 1
        else:
            frequency_edge[edge_string] = 1

    weighted_edges = []
    for edge_string, weight in frequency_edge.iteritems():
        edge = literal_eval(edge_string)
        weighted_edges.append(edge + (float(weight),))
    graph.add_weighted_edges_from(weighted_edges)
    return graph
