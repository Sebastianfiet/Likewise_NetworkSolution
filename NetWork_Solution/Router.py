import socket
import threading

class Router:
    """
    A class to represent the network routers.

    Attributes:
    - controller_host (str): The IP address of the network controller.
    - controller_port (int): The port number of the network controller.
    - dijkstra_host (str): The IP address of the Dijkstra Algorithm Server.
    - dijkstra_port (int): The port number of the Dijkstra Algorithm Server.
    - controller_socket: The socket object for communication with the network controller.
    - dijkstra_socket: The socket object for communication with the Dijkstra Algorithm Server.
    - running (bool): A flag indicating if the router is running.

    Methods:
    - __init__(self, controller_host, controller_port, dijkstra_host, dijkstra_port): Initializes a Router object.
    - connect_to_controller(self): Connects the router to the network controller.
    - connect_to_dijkstra(self): Connects the router to the Dijkstra Algorithm Server.
    - receive_message(self): Receives messages from the network controller and processes them.
    - start(self): Starts the router by connecting to the controller and Dijkstra server, and starts message receiving.


    """

    def __init__(self, controller_host, controller_port, dijkstra_host, dijkstra_port):
        """
        Initializes a Router object.

        Parameters:
        - controller_host (str): The IP address of the network controller.
        - controller_port (int): The port number of the network controller.
        - dijkstra_host (str): The IP address of the Dijkstra Algorithm Server.
        - dijkstra_port (int): The port number of the Dijkstra Algorithm Server.
        """
        self.controller_host = controller_host
        self.controller_port = controller_port
        self.dijkstra_host = dijkstra_host
        self.dijkstra_port = dijkstra_port
        self.controller_socket = None
        self.dijkstra_socket = None
        self.running = True

    def connect_to_controller(self):
        """
        Connects the router to the controller.
        """
        print("Connecting to controller...")
        self.controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controller_socket.bind(('localhost', 0))
        ip, port = self.controller_socket.getsockname()
        print(f"Router connected to controller at {ip}:{port}")
        self.controller_socket.connect((self.controller_host, self.controller_port))

    def connect_to_dijkstra(self):
        """
        Connects the router to the Dijkstra Algorithm Server (It uses BellMan Ford as well, but the name stayed).
        """
        print("Connecting to Dijkstra Algorithm Server...")
        self.dijkstra_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dijkstra_socket.bind(('localhost', 0))
        ip, port = self.dijkstra_socket.getsockname()
        print(f"Router connected to Dijkstra Algorithm Server at {ip}:{port}")
        self.dijkstra_socket.connect((self.dijkstra_host, self.dijkstra_port))

    def receive_message(self):
        """
        Receives messages from the network controller and processes them. What it does is removing one of the headers of
        the message (The header that corresponds to the router) and then send it back to the controller, so the latter
        can send that message to another router and repeat this process over and over again, until the message finally
        gets to the client.
        """
        while self.running:
            try:
                data = self.controller_socket.recv(16777216).decode()
                if data:
                    print(f"Received message from controller: {data}")
                    # Remove the first header if it matches the Dijkstra socket
                    if data.startswith(f"{self.dijkstra_socket.getsockname()[0]}:{self.dijkstra_socket.getsockname()[1]}"):
                        data = ','.join(data.split(',')[1:])
                    # Send back the modified message to the controller
                    self.controller_socket.sendall(data.encode())
            except Exception as e:
                print(f"Error receiving or sending message: {e}")
                break

    def start(self):
        """
        Starts the router by connecting it to the controller and Dijkstra server. This function also starts its message
        receiving capabilities.
        """
        self.connect_to_controller()
        self.connect_to_dijkstra()

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        # Wait for the thread to finish
        receive_thread.join()

        # Close the sockets
        self.controller_socket.close()
        self.dijkstra_socket.close()

# Example usage
if __name__ == "__main__":
    router = Router("localhost", 9999, "localhost", 65432)
    router.start()
