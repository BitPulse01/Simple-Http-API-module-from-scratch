from threading import Thread, active_count
from typing import Any
from colorama import Fore
from os import stat
import socket


class __request:
    def __init__(self, request: bytes, Endpoints: list[str], endpoint: dict[str, str]) -> None:
        request = request.decode()
        self.endpoints_dict = endpoint
        self.REQUEST_DATA: list[str] = request.split('\r\n')
        self.REQUEST_endpoint_DATA: list[str] = self.REQUEST_DATA[0].split(' ')
        self.REQUEST_HEADER: list[str] = request.split('\r\n')[1].split(": ")
        
        self.message: bytes = b""

        self.REQUEST_DATA = {
            "method" : self.REQUEST_endpoint_DATA[0],
            "endpoint" : self.REQUEST_endpoint_DATA[1],
            "HTTP_version" : self.REQUEST_endpoint_DATA[2],
            "user_agent" : self.REQUEST_HEADER[1], 
        }

        self.ENDPOINTS: list[str] = Endpoints

    def handel_endpoints(self):
        for _, endpoint in enumerate(self.ENDPOINTS):
            if self.REQUEST_DATA['endpoint'] == endpoint:
                for _, endpoint in enumerate(self.endpoints_dict):
                    if self.REQUEST_DATA['endpoint'] == endpoint:
                        self.content = self.endpoints_dict[endpoint]

                self.message = b'HTTP/1.1 200 OK\r\n\r\n' + str(self.content).encode()

                return self.message
                break


        else:
            self.message = b'HTTP/1.1 404 Not Found\r\n\r\n'
            return self.message
        
class API:
    def __init__(self, endpoints: list[str], endpoint_data: dict[str, Any]) -> None:
        self.endpoints = endpoints
        self.endpoints_data = endpoint_data
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", 4221))
            print(Fore.GREEN + "server running on http://localhost:4221")
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            server_socket.listen()

            while True:
                connection, address = server_socket.accept() # wait for client

                thread: Thread = Thread(target= self.start, args=(connection, ))
                thread.start()   
            
    def start(self, connection: socket.socket):
        REQUEST: bytes = connection.recv(1048)
        REQUEST_HANDELER = __request(REQUEST, self.endpoints, self.endpoints_data)
        MESSAGE: bytes = REQUEST_HANDELER.handel_endpoints()
        
        print(Fore.MAGENTA + "---------------------")
        print(Fore.GREEN + REQUEST.decode())
        print(Fore.MAGENTA + "---------------------")
        print(Fore.CYAN + MESSAGE.decode())
        print(Fore.MAGENTA + "---------------------")
    
        connection.sendall(MESSAGE)
