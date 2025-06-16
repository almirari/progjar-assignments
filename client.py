from socket import socket, AF_INET, SOCK_STREAM

SERVER_ADDRESS = ('localhost', 45000)
BUFFER_SIZE = 32
TIME_CMD = "TIME"
QUIT_CMD = "QUIT"

def main():
    try:
        with socket(AF_INET, SOCK_STREAM) as client_socket:
            client_socket.connect(SERVER_ADDRESS)

            while True:
                message = input("Enter command (TIME or QUIT): ").strip().upper()

                if message == TIME_CMD:
                    client_socket.sendall(f"{TIME_CMD}\r\n".encode('utf-8'))
                    response = client_socket.recv(BUFFER_SIZE)
                    print("Server:", response.decode('utf-8').strip())

                elif message == QUIT_CMD:
                    client_socket.sendall(f"{QUIT_CMD}\r\n".encode('utf-8'))
                    print("Connection closed.")
                    break

                else:
                    print("Invalid command. Please enter TIME or QUIT.")

    except KeyboardInterrupt:
        print("\nInterrupted by user. Closing connection.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

