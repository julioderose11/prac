import hashlib
import socketserver
from typing import Tuple

__all__ = ["CS3CPServer"]


class CS3CPRequestHandler(socketserver.DatagramRequestHandler):
    def send_reponse(self, code: int, message: str):
        self.wfile.write(f"{code} {message}".encode())

    def trigger_action(self, action: str, args):
        self.server.actions.append((action, args))

    def handle(self):
        command, identifier, _ = self.rfile.readline().decode().split()  # identifies which command was issued and
        # acts accordingly.

        if command not in ["CHAT", "CONNECT", "DISCONNECT"]:
            self.send_reponse(400, "UNKNOWN_COMMAND")  # if command is not recognised server feedback is returned.
            return

        if command == "CHAT":
            sha = self.rfile.readline().decode().split()[1]  # decrypts the message
            message = self.rfile.readline().decode()  # decodes message

            if sha == hashlib.sha256(message.encode(
                    'utf-8')).hexdigest():  # uses hash function to check if the final message is the same and
                # ensures no values are lost.

                self.trigger_action("CHAT",
                                    [self.client_address, identifier, message])  # server sends message to client
                self.send_reponse(203, "RECEIVED")  # notifies that message was received

        if command == "CONNECT":
            self.trigger_action("CONNECT", (identifier, self.client_address))  # connects to client address

            self.send_reponse(200, "OK")  # server feedback for connecting to client

        if command == "DISCONNECT":
            self.trigger_action("DISCONNECT", identifier)  # disconnects from client
            self.send_reponse(200, "OK")  # server feedback for disconnecting from client


class CS3CPServer(socketserver.ThreadingUDPServer):
    def __init__(self, server_address: Tuple[str, int]) -> None:
        super().__init__(server_address, CS3CPRequestHandler)
        self.clients = {}
        self.actions = []

    def service_actions(self):
        while len(self.actions) > 0:
            action, args = self.actions.pop()
            if action == "CHAT":
                from_addr, to_name, body = args
                to_addr = self.clients[to_name]

                from_name = list(self.clients.keys())[list(self.clients.values()).index(from_addr)]

                self.socket.sendto(f"{from_name}: {body}".encode(), to_addr)
                # self.socket.sendto("205 DELIVERED".encode(), from_addr)

            if action == "CONNECT":
                username, address = args
                self.clients[username] = address
                print(f"{username} connected")

            if action == "DISCONNECT":
                username = args
                del self.clients[username]
                print(f"{username} disconnected")
