import socket
import sys


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 12345)  # Change the port if necessary
print('Connecting to {} port {}'.format(*server_address))
client_socket.connect(server_address)

try:
    # Send data
    number = int(input("Enter a number to calculate factorial: "))
    client_socket.sendall(str(number).encode())

    # Receive the response
    response = client_socket.recv(1024)
    print('Factorial:', response.decode())

finally:
    # Clean up the connection
    client_socket.close()
