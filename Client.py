import hashlib
import socket
from typing import Tuple


class CS3CPClient:
    __version__ = "CS3CP/0.1"
    __bufsize = 2048

    def __init__(self, server_address: Tuple[str, int]) -> None:
        self.server_address = server_address
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # initialises a UDP socket.

    def listen(self) -> str:
        reply, _ = self.socket.recvfrom(self.__bufsize)  # waits and receives message.

        return reply.decode()

    def _send_request(self, data: str) -> str:  # sends decoded data to server.
        self.socket.sendto(data.encode(), self.server_address)
        reply, _ = self.socket.recvfrom(self.__bufsize)

        return reply.decode()

    def connect(self, username: str) -> str:  # connect command allocates a username value and sends it to server
        self.username = username
        data = f"CONNECT {self.username} {self.__version__}"  # stores user's username.
        return self._send_request(data)  # sends username to server.

    def chat(self, recipient: str, message: str) -> str:  # initializes chat message between client and recipient
        sha = hashlib.sha256(message.encode("utf-8")).hexdigest()  # encrypts message
        data = f"CHAT {recipient} {self.__version__}\r\nSHA: {sha}\r\n{message}"
        return self._send_request(data)

    def disconnect(self) -> str:  # disconnects client
        data = f"DISCONNECT {self.username} {self.__version__}"
        resp = self._send_request(data)
        self.socket.close()

        return resp
