

   ```python
   # server.py
   import socket

   def start_server(port):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
           server_socket.bind(('localhost', port))
           server_socket.listen(1)
           print(f"Listening for incoming connections on port {port}...")
           conn, addr = server_socket.accept()
           with conn:
               print(f"Connected by {addr}")
               data = conn.recv(1024)
               print("Received data:")
               print(data.decode())

   if __name__ == "__main__":
       port = int(input("Enter the port to listen on: "))
       start_server(port)
