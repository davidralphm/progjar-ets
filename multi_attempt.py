import os
from socket import *
import socket
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import time
import sys
import logging
import ssl

from http import HttpServer

httpserver = HttpServer()


def ProcessTheClient(connection, addr):
	rcv=""

	while True:
		try:
			data = connection.recv(32)

			if data:
				d = data.decode()
				rcv=rcv+d

				if rcv[-2:]=='\r\n':
					hasil = httpserver.proses(rcv)
					hasil=hasil+"\r\n\r\n".encode()
					connection.sendall(hasil)
					rcv=""
					break
			else:
				break

		except OSError as e:
			pass

	connection.close()

class Server(hostname='testing.net'):
	cert_location = os.getcwd() + '/certs/'
	context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
	context.load_cert_chain(certfile=cert_location + 'domain.crt', keyfile=cert_location + 'domain.key')

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	my_socket.bind(('0.0.0.0', 8443))
	my_socket.listen(1)

	with ProcessPoolExecutor(20) as executor:
		while True:
			connection, client_address = my_socket.accept()
			try:
				secure_connection = context.wrap_socket(connection, server_side=True)
				p = executor.submit(ProcessTheClient, secure_connection, client_address)
			except ssl.SSLError as essl:
				print(str(essl))


def main():
	Server()

if __name__=="__main__":
	main()

