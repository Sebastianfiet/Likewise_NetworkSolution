import networkx as nx
import matplotlib.pyplot as plt
from node import Node
from link import Link
import socket


class Network:
    """
    A class to represent a computer network.

    Attributes:
    - nodes (dict): A dictionary containing nodes in the network, with node ID as keys and Node objects as values.
    - links (list): A list containing Link objects representing links between nodes.
    - graph (NetworkX graph): A graph representing the network topology.
    - server_socket (socket.socket): The server socket for accepting connections.
    - host (str): The host IP address for the server socket.
    - port (int): The port number for the server socket.

    Methods:
    - __init__(self): Initializes a Network object.
    - initialize_server(self): Initializes the server socket for accepting connections.
    - accept_connections(self): Accepts connections from nodes and assigns IP and port.
    - add_node(self, node_id, name, node_type='router'): Adds a new node to the network.
    - add_link(self, source_id, destination_id, bandwidth): Adds a link between two nodes in the network.
    - remove_node(self, node_id): Removes a node and its associated links from the network.
    - display_network(self): Displays information about nodes and links in the network.
    - visualize_network(self): Visualizes the network topology using Matplotlib.
    """

    def __init__(self):
        """
        Initializes a Network object.
        """
        self.nodes = {}
        self.links = []
        self.graph = nx.Graph()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = '127.0.0.1'  # Localhost
        self.port = 12345  # Starting port
        self.initialize_server()

    def initialize_server(self):
        """
        Initializes the server socket for accepting connections.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

    def accept_connections(self):
        """
        Accepts connections from nodes and assigns IP and port.
        """
        node_names = list(self.nodes.keys())
        current_index = 0

        while current_index < len(node_names):
            client_socket, addr = self.server_socket.accept()
            print(f"Connected by {addr}")
            node = self.nodes[node_names[current_index]]
            node.ip, node.port = addr
            current_index += 1

            client_socket.sendall(f"You are connected as {node.name} with IP {addr[0]} and Port {addr[1]}".encode())

    def add_node(self, node_id, name, node_type='router'):
        """
        Adds a new node to the network.

        Parameters:
        - node_id (int): The ID of the node.
        - name (str): The name of the node.
        - node_type (str): The type of the node (default is 'router').
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = Node(node_id, name, node_type)
            self.graph.add_node(name, node_type=node_type)

    def add_link(self, source_id, destination_id, bandwidth):
        """
        Adds a link between two nodes in the network.

        Parameters:
        - source_id (int): The ID of the source node.
        - destination_id (int): The ID of the destination node.
        - bandwidth (int): The bandwidth of the link in Gbps.
        """
        if source_id in self.nodes and destination_id in self.nodes:
            inverse_weight = 1.0 / bandwidth if bandwidth != 0 else float('inf')
            self.links.append(Link(self.nodes[source_id], self.nodes[destination_id], bandwidth))
            self.graph.add_edge(self.nodes[source_id].name, self.nodes[destination_id].name, weight=inverse_weight)
        else:
            print("Error: One or both nodes not found in the network.")

    def remove_node(self, node_id):
        """
        Removes a node and its associated links from the network.

        Parameters:
        - node_id (int): The ID of the node to be removed.
        """
        if node_id in self.nodes:
            node_name = self.nodes[node_id].name
            self.graph.remove_node(node_name)
            del self.nodes[node_id]
            # Remove any links associated with this node
            self.links = [link for link in self.links if
                          link.source.node_id != node_id and link.destination.node_id != node_id]
            print(f"Node {node_name} and its associated links have been removed from the network.")
        else:
            print(f"Node ID {node_id} not found in the network.")

    def display_network(self):
        """
        Displays information about nodes and links in the network.
        """
        print("Nodes in the network:")
        for node in self.nodes.values():
            print(node)
        print("\nLinks in the network:")
        for link in self.links:
            print(link)

    def visualize_network(self):
        """
        Visualizes the network topology using Matplotlib.
        """
        pos = nx.spring_layout(self.graph)  # positions for all nodes
        nx.draw(self.graph, pos, with_labels=True, node_size=3000, node_color="violet", font_size=15, font_weight="bold")
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()
