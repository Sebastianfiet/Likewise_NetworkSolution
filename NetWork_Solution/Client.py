import socket
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

class Client:
    """
    A class to represent a network client.

    Attributes:
    - controller_host (str): The IP address of the network controller.
    - controller_port (int): The port number of the network controller.
    - dijkstra_host (str): The IP address of the Dijkstra Algorithm Server.
    - dijkstra_port (int): The port number of the Dijkstra Algorithm Server.
    - controller_socket: The socket object for communication with the network controller.
    - dijkstra_socket: The socket object for communication with the Dijkstra Algorithm Server.
    - running (bool): A flag indicating if the client is running.
    - public_key_file (str): The file path of the public key.
    - private_key_file (str): The file path of the private key.
    - public_key: The public key used to encrypt the message.
    - private_key: The private key used to decrypt the message.

    Methods:
    - __init__(self, controller_host, controller_port, dijkstra_host, dijkstra_port): Initializes a Client object.
    - connect_to_controller(self): Connects the client to the network controller.
    - connect_to_dijkstra(self): Connects the client to the Dijkstra Algorithm Server.
    - load_key_pair(self): Loads the public and private key pair from the project folder.
    - encrypt_message(self, message, public_key): Encrypts the message using the public key.
    - send_encrypted_message(self): Sends an encrypted message to the controller.
    - receive_message(self): Receives messages from the network controller and prints them.
    - decrypt_message(self, encrypted_message): Decrypts the encrypted message using the private key.
    - send_audio_file(self): Sends an audio file to the controller.
    - save_audio_file(self, data): Saves the received audio file.
    - start(self): Starts the client by connecting to the controller and Dijkstra server. This function also starts
    its message sending and receiving capabilities.
    """
    def __init__(self, controller_host, controller_port, dijkstra_host, dijkstra_port):
        """
        Initializes a Client object.

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
        self.public_key_file = "public_key.pem"
        self.private_key_file = "private_key.pem"

    def connect_to_controller(self):
        """
        Connects the client to the network controller.
        """
        self.controller_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.controller_socket.connect((self.controller_host, self.controller_port))
        print(f"Client connected to controller at {self.controller_host}:{self.controller_port}")

    def connect_to_dijkstra(self):
        """
        Connects the client to the Dijkstra Algorithm Server.
        """
        self.dijkstra_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dijkstra_socket.connect((self.dijkstra_host, self.dijkstra_port))
        print(f"Client connected to Dijkstra Algorithm Server at {self.dijkstra_host}:{self.dijkstra_port}")

    def load_key_pair(self):
        """
        Loads the public and private key pair from the project folder.
        """
        with open(self.public_key_file, "rb") as file:
            self.public_key = file.read()

        with open(self.private_key_file, "rb") as file:
            self.private_key = file.read()

    def encrypt_message(self, message, public_key):
        """
        Encrypts the message using the public key.

        Parameters:
        - message (str): The message to be encrypted.
        - public_key (str): The public key used for the encryption.

        Returns:
        - encrypted_message: The encrypted message.
        """
        cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
        encrypted_message = cipher.encrypt(message.encode())
        return encrypted_message

    def send_encrypted_message(self):
        """
        Sends the encrypted message to the controller.
        """
        while self.running:
            message = input("Enter message to send to controller: ")
            if message:
                if message.lower() == "audiofile":
                    self.send_audio_file()
                else:
                    try:
                        encrypted_message = self.encrypt_message(message, self.public_key)
                        # Encode encrypted message as base64
                        encoded_message = base64.b64encode(encrypted_message)
                        self.controller_socket.sendall(encoded_message)
                    except Exception as e:
                        print(f"Error sending message to controller: {e}")


    def receive_message(self):
        """
        Receives messages from the network controller and processes them. If it's more than 1000 characters long, that
        means it's an audio file, so it calls the corresponding function to save it. If it's not more than 1000
        characters long, it's just a regular message, so it decrypts it using the private key and prints it.
        """
        while self.running:
            try:
                data = self.controller_socket.recv(16777216)
                if data:
                    # Check if the received data is an audio file (base64 encoded)
                    if len(data) > 1000:
                        print("Received audio file from controller.")
                        self.save_audio_file(data)
                    else:
                        print("Received encrypted message from controller.")
                        print("Decrypting message...")
                        decoded_message = base64.b64decode(data)
                        decrypted_message = self.decrypt_message(decoded_message)
                        print(f"Decrypted message from controller: {decrypted_message}")
            except Exception as e:
                print(f"Error receiving message from controller: {e}")

    def decrypt_message(self, encrypted_message):
        """
        Decrypts the incoming encrypted message using the private key.

        Parameters:
        - encrypted_message: The encrypted message.

        Returns:
        - decrypted_message: The decrypted message.
        """
        key = RSA.import_key(self.private_key)
        cipher = PKCS1_OAEP.new(key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode()

    def send_audio_file(self):
        """
        Sends an audio file to the controller. It sends it as a string instead of bytes for simplicity.
        """
        file_path = input("Enter the path of the audio file: ")
        with open(file_path, "rb") as file:
            audio_data = file.read()
        # Encode the audio data as base64
        encoded_audio = base64.b64encode(audio_data)
        # Send the encoded audio data to the controller
        self.controller_socket.sendall(encoded_audio)

    def save_audio_file(self, data):
        """
        Saves the received audio file.

        Parameters:
        - data (bytes): The audio file data received from the controller.
        """
        audio_data = base64.b64decode(data)
        with open("received_audio.wav", 'wb') as file:
            file.write(audio_data)
        print("Audio file received and saved successfully.")

    def start(self):
        """
        Starts the client by connecting to the controller and Dijkstra server. This function also starts the client's
        message sending and receiving capabilities.
        """
        self.connect_to_controller()
        self.connect_to_dijkstra()
        self.load_key_pair()

        # Start a thread to send messages
        send_thread = threading.Thread(target=self.send_encrypted_message)
        send_thread.start()

        # Start a thread to receive messages
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        # Wait for the threads to finish
        send_thread.join()
        receive_thread.join()

        # Close the sockets
        self.controller_socket.close()
        self.dijkstra_socket.close()

# Example usage
if __name__ == "__main__":
    client = Client("localhost", 9999, "localhost", 65432)
    client.start()
