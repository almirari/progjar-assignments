from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import threading
import logging
import time

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        super().__init__()
        self.connection = connection
        self.address = address

    def run(self):
        try:
            while True:
                data = self.connection.recv(32)
                if not data:
                    break

                message = data.decode('utf-8').strip()
                logging.info(f"Received from {self.address}: {message}")

                if message == "TIME":
                    current_time = time.strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    self.connection.sendall(response.encode('utf-8'))

                elif message == "QUIT":
                    break

                else:
                    logging.warning(f"Unknown command from {self.address}: {message}")
        except Exception as e:
            logging.warning(f"Error with client {self.address}: {e}")
        finally:
            logging.info(f"Client {self.address} disconnected.")
            self.connection.close()


class Server(threading.Thread):
    def __init__(self):
        super().__init__()
        self.the_clients = []
        self.my_socket = socket(AF_INET, SOCK_STREAM)
        self.my_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.warning("Server is listening on port 45000...")

        try:
            while True:
                conn, addr = self.my_socket.accept()
                logging.info(f"Connection from {addr}")
                client_thread = ProcessTheClient(conn, addr)
                client_thread.start()
                self.the_clients.append(client_thread)
        except KeyboardInterrupt:
            logging.warning("Server shutdown requested.")
        finally:
            self.my_socket.close()
            for t in self.the_clients:
                t.join()
            logging.warning("Server closed all connections.")


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    server = Server()
    server.start()

if __name__ == "__main__":
    main()

