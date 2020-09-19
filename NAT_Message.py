import socket,threading

class server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        net_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("test_server")
        net_socket.bind(("0.0.0.0",2345))
        net_socket.listen(1)
        try:
            while True:
                client,address = net_socket.accept()
                print(address)
                data = client.recv(1024)
                print("from other:",data.decode())
                client.close()
        except Exception as e:
            print("error_server",str(e))

class client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        net_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("test_client")
        #address = "x.x.x.x"
        try:
            while True:
                address = input("connect ip:")
                net_socket.connect((address,2345))
                text = input("Message for {}:".format(address))
                net_socket.send(text.encode())
                net_socket.close()
        except Exception as e:
            print("error_client:",str(e))
        

if __name__ == '__main__':
    
    server = server()
    client = client()

    server.start()
    client.start()
