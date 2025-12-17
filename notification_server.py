"""
TCP Notification Server
A simple TCP server that receives notifications from the email client.
Course: Computer Networks - Fall 2025
"""

import socket


def start_server(host='127.0.0.1', port=9999):
    """Start the TCP notification server."""
    # Create TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # Bind and listen
        server_socket.bind((host, port))
        server_socket.listen(5)

        print("="*40)
        print("TCP NOTIFICATION SERVER")
        print("="*40)
        print(f"Listening on {host}:{port}")
        print("Press Ctrl+C to stop.")
        print("="*40 + "\n")

        while True:
            # Accept connection
            client_socket, address = server_socket.accept()
            print(f"[+] Connection from {address}")

            try:
                # Receive message
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    print(f"[NOTIFICATION] {message}")
                    print("-"*30)
            except Exception as e:
                print(f"[!] Error: {e}")
            finally:
                client_socket.close()

    except KeyboardInterrupt:
        print("\n[*] Shutting down...")
    except Exception as e:
        print(f"[!] Server error: {e}")
    finally:
        server_socket.close()
        print("[*] Server closed.")


if __name__ == "__main__":
    print("\nStarting Notification Server...")
    start_server()
