import cv2
import numpy as np
import socket
import pickle
import struct

# Host and port for the server
HOST = '192.168.22.98'  # Change this to the IP of the receiver
PORT = 9999

# Initialize OpenCV camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("Server")  # Create a window to display the colored camera feed

# Set up socket connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}")

while True:
    # Accept a connection
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} established")

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.resize(frame, (640, 480))

        # Convert the frame to black and white
        bw_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Display the original colored frame in the "Server" window
        cv2.imshow(f"Server sending to {addr}", frame)

        # Serialize the black and white frame
        bw_data = pickle.dumps(bw_frame)
        message_size = struct.pack("L", len(bw_data))  # Format message size as unsigned long

        # Send message size first
        client_socket.sendall(message_size)

        # Send the serialized black and white frame
        client_socket.sendall(bw_data)

        # Check for 'q' key to quit streaming
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the connection
    cap.release()
    client_socket.close()
    break  # Close the server after streaming is done

# Close the server socket
server_socket.close()
cv2.destroyAllWindows()