class Node:
    """
    A class to represent a network node.

    Attributes:
    - node_id (int): The unique identifier of the node.
    - name (str): The name of the node.
    - node_type (str): The type of the node, defaults to 'router'.

    Methods:
    - __init__(self, node_id, name, node_type='router'): Initializes a Node object with the given attributes.
    - __repr__(self): Returns a string representation of the Node object.
    """

    def __init__(self, node_id, name, node_type='router'):
        """
        Initializes a Node object with the given attributes.

        Parameters:
        - node_id (int): The unique identifier of the node.
        - name (str): The name of the node.
        - node_type (str): The type of the node, defaults to 'router'.
        """
        self.node_id = node_id
        self.name = name
        self.node_type = node_type

    def __repr__(self):
        """
        Returns a string representation of the Node object.

        Returns:
        - str: A string representing the Node object.
        """
        return f"Node({self.name}, ID={self.node_id}, Type={self.node_type})"