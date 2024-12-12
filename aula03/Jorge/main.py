import socket

addr = "0.0.0.0"
port = 666

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((addr, port))
    s.listen(1)
    conn, client_addr = s.accept()
    with conn:
        print('Connected by', client_addr)
        while True:
            data = conn.recv(1024)
            data = data.decode("utf-8")

            if data.lower() =="exit":
                conn.send(b"exit")
                break
            # if not data: 
            #     break      
            conn.sendall(data)

