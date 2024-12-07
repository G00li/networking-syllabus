import socket

addr = "0.0.0.0"
port = 666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((addr, port))
    s.listen(1)
    print(f"Server listening on {addr}:{port}")
    conn, client_addr = s.accept()
    with conn:
        print('Connected by', client_addr)
        while True:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected")
                break 
            decoded_data = data.decode('utf-8').strip()
            print(f"Received: {decoded_data}")
            if decoded_data.lower() == "exit":
                conn.send(b"exit")
                print("Exiting connection")
                break
            conn.sendall(data)
