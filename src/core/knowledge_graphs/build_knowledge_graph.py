import networkx as nx
import matplotlib.pyplot as plt


def get_graph(data):
    G = nx.DiGraph()

    for item in data:
        G.add_edge(item['head'], item['tail'], relation=item['type'])
    return G