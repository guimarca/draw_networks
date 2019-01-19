import csv
import os
import networkx
import numpy as np

import matplotlib.pyplot as plt
from numpy import genfromtxt


class NetworkDrawer:
    BASE_NODE_SIZE = 200
    INCREASE_NODE_SIZE = 100
    SHOW_TITLE = False
    LABELS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
    COLORS = {
        '0': 'salmon',  # minority
        '1': 'skyblue'  # majority
    }
    SHAPES = {
        '0': 'v',  # triangle (for square use 's')
        '1': 'o'  # circle
    }

    def __init__(self, filename, N, NG, NP, show_trials):
        os.chdir(os.path.dirname(__file__))
        self.data = genfromtxt('input_files/' + filename, delimiter=',', skip_header=1)
        self.N = N
        self.NP = NP
        self.NG = NG
        self.show_trials = show_trials
        self.LABELS = self.make_label_dict(self.LABELS)

    @staticmethod
    def get_treatment_name(group):
        if group in ['111', '112', '113', '411', '412', '413']:
            return "ENDO_HIGH"
        elif group in ['331', '332', '333', '631', '632', '633']:
            return "ENDO_LOW"
        elif group in ['951', '952', '953', '1051', '1052', '1053']:
            return "ENDO_HIGH_FREE"
        elif group in ['1161', '1162', '1163', '1261', '1262', '1263']:
            return "ENDO_HIGH_CHEAP"
        elif group in ['221', '222', '223', '521', '522', '523']:
            return "EXO_HIGH"
        elif group in ['741', '742', '743', '841', '842', '843']:
            return "EXO_LOW"
        else:
            return "G"

    @staticmethod
    def column(matrix, i):
        return [str(int(row[i])) for row in matrix[0:]]

    @staticmethod
    def get_labels(csvfile):
        with open(csvfile) as f:
            reader = csv.reader(f)
            # get the first line in csv
            labels = reader.next()
        # return just the letters from pos 1 on
        return labels[1:]

    @staticmethod
    def make_label_dict(labels):
        l = {}
        for i, label in enumerate(labels):
            l[i] = label
        return l

    @staticmethod
    def interchange_positions(pos, p1, p2):
        aux = pos[p1]
        pos[p1] = pos[p2]
        pos[p2] = aux
        return pos

    def draw_in_image_files(self):
        offset = 0
        for n_group in range(1, self.NG + 1):  # Group iteration
            for n_period in range(1, self.NP + 1):  # Period iteration
                adjacency = self.data[offset:offset + self.N, 1:self.N + 1]

                types = self.column(self.data[offset:offset + self.N, self.N + 1:self.N + 2], 0)
                types = types[:]

                actions = self.column(self.data[offset:offset + self.N, self.N + 2:self.N + 3], 0)
                actions = actions[:]

                group = str(int(self.data[offset, 0]))
                period = str(int(self.data[offset, self.N + 3]))
                offset = offset + self.N

                if self.show_trials or int(period) > 0:
                    self.generate_graph_with_labels(adjacency, types, actions)
                    self.generate_image_file(group, period)

    def generate_graph_with_labels(self, adjacency_matrix, types, actions):
        plt.axes([0, 0, 1, 1])
        G = networkx.Graph()

        # Adding nodes to the network
        for player in range(0, self.N):
            G.add_node(player + 1, label=self.LABELS[player], type=types[player],
                       shape=self.SHAPES.get(types[player]), color=self.COLORS.get(actions[player]))

        # Grouping players by type: circles (1) left
        pos = networkx.circular_layout(G)
        '''
        pos = interchange_positions(pos, 2, 6)
        pos = interchange_positions(pos, 13, 15)
        pos = interchange_positions(pos, 3, 10)
        pos = interchange_positions(pos, 12, 14)
        '''

        # Draw node labels
        networkx.draw_networkx_labels(G, pos)

        # Adding links to the network
        rows, cols = np.where(adjacency_matrix == 1)
        rows = rows+1
        cols = cols+1
        edges = zip(rows.tolist(), cols.tolist())
        # sys.exit()
        G.add_edges_from(edges)

        networkx.draw_networkx_edges(G, pos, width=0.3)

        for player in G.nodes():
            networkx.draw_networkx_nodes(G, pos, [G.nodes()[player - 1]],
                                   node_size=self.BASE_NODE_SIZE + self.INCREASE_NODE_SIZE * G.degree(player),
                                   node_shape=G.node[player]['shape'],
                                   node_color=G.node[player]['color'],
                                   label=G.node[player]['label'])

    def generate_image_file(self, group, period):
        name_file = self.get_treatment_name(group) + "_" + str(group) + "_" + str(period) + ".png"
        print("Generating image: " + name_file)

        # Show graph title
        if self.SHOW_TITLE:
            plt.title(self.get_treatment_name(group) + "  " + str(period))

        plt.axis('off')
        plt.savefig("output_img/" + name_file, format="PNG")
        plt.close()
