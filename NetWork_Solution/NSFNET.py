from network import Network

class NSFNET:
    """
    A class representing the NSFNET topology.

    Attributes:
    - network (Network): The underlying network instance representing the NSFNET.

    Methods:
    - __init__(self): Initializes an instance of the NSFNET class.
    - setup_topology(self): Sets up the nodes and links for the NSFNET.
    """

    def __init__(self):
        """
        Initializes an instance of the NSFNET class.
        """
        self.network = Network()

    def setup_topology(self):
        """
        Sets up the nodes and links for the NSFNET.
        """
        # Add the Nodes.
        self.network.add_node(1, 'WA')
        self.network.add_node(2, 'CA1')
        self.network.add_node(3, 'CA2')
        self.network.add_node(4, 'UT')
        self.network.add_node(5, 'CO')
        self.network.add_node(6, 'TX')
        self.network.add_node(7, 'NE')
        self.network.add_node(8, 'IL')
        self.network.add_node(9, 'PA')
        self.network.add_node(10, 'GA')
        self.network.add_node(11, 'MI')
        self.network.add_node(12, 'NY')
        self.network.add_node(13, 'NJ')
        self.network.add_node(14, 'DC')

        # Add the Links between Nodes.
        self.network.add_link(1, 2, 2100)  # Link With 2100 Gbps bandwidth.
        self.network.add_link(1, 3, 3000)  # Link With 3000 Gbps bandwidth.
        self.network.add_link(1, 8, 4800)  # Link With 4800 Gbps bandwidth.
        self.network.add_link(2, 3, 1200)  # Link With 1200 Gbps bandwidth.
        self.network.add_link(2, 4, 1500)  # Link With 1500 Gbps bandwidth.
        self.network.add_link(3, 6, 3600)  # Link With 3600 Gbps bandwidth.
        self.network.add_link(4, 5, 1200)  # Link With 1200 Gbps bandwidth.
        self.network.add_link(4, 11, 3900)  # Link With 3900 Gbps bandwidth.
        self.network.add_link(5, 6, 2400)  # Link With 2400 Gbps bandwidth.
        self.network.add_link(5, 7, 1200)  # Link With 1200 Gbps bandwidth.
        self.network.add_link(6, 10, 2100)  # Link With 2100 Gbps bandwidth.
        self.network.add_link(6, 14, 3600)  # Link With 3600 Gbps bandwidth.
        self.network.add_link(7, 8, 1500)  # Link With 1500 Gbps bandwidth.
        self.network.add_link(7, 10, 2700)  # Link With 2700 Gbps bandwidth.
        self.network.add_link(8, 9, 1500)  # Link With 1500 Gbps bandwidth.
        self.network.add_link(9, 10, 1500)  # Link With 1500 Gbps bandwidth.
        self.network.add_link(9, 12, 600)  # Link With 600 Gbps bandwidth.
        self.network.add_link(9, 13, 600)  # Link With 600 Gbps bandwidth.
        self.network.add_link(11, 12, 1200)  # Link With 1200 Gbps bandwidth.
        self.network.add_link(11, 13, 1500)  # Link With 1200 Gbps bandwidth.
        self.network.add_link(12, 14, 600)  # Link With 600 Gbps bandwidth.
        self.network.add_link(13, 14, 300)  # Link With 600 Gbps bandwidth.

        # Display network information and visualize the network.
        self.network.display_network()
        self.network.visualize_network()

# Example usage
if __name__ == "__main__":
    nsfnet = NSFNET()
    nsfnet.setup_topology()
