import socket
import os

HOST = '127.0.0.1'
PORT = 8805

def send_request(request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request.encode())
        response = s.recv(1024 * 100).decode()
        print(response)

def list_files():
    request = "GET /list HTTP/1.0\r\n\r\n"
    send_request(request)

def upload_file(filepath):
    if not os.path.isfile(filepath):
        print("File does not exist.")
        return

    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        file_data = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    content_type = f"multipart/form-data; boundary={boundary}"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

    request = (
        f"POST /upload HTTP/1.0\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
    ).encode() + body

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(request)
        response = s.recv(1024 * 100).decode()
        print(response)

def delete_file(filename):
    request = f"DELETE /delete?filename={filename} HTTP/1.0\r\n\r\n"
    send_request(request)

def main_menu():
    while True:
        print("\n--- File Client Menu ---")
        print("1. List files")
        print("2. Upload file")
        print("3. Delete file")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            list_files()
        elif choice == '2':
            filepath = input("Enter the path to the file to upload: ").strip()
            upload_file(filepath)
        elif choice == '3':
            filename = input("Enter the filename to delete: ").strip()
            delete_file(filename)
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main_menu()
