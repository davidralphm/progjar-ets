import os
from socket import *
import socket
import multiprocessing
import time
import sys
import logging
from concurrent.futures import ProcessPoolExecutor
import ssl

from http import HttpServer

httpserver = HttpServer()

#untuk menggunakan processpoolexecutor, karena tidak mendukung subclassing pada process,
#maka class ProcessTheClient dirubah dulu menjadi function, tanpda memodifikasi behaviour didalamnya

def ProcessTheClient(connection,address):
	# Buat secure connection
	connection = ssl.wrap_socket(connection, './certs/domain.key', './certs/domain.crt', True)

	rcv=""

	while True:
		try:
			data = connection.recv(32)
			if data:
				#merubah input dari socket (berupa bytes) ke dalam string
				#agar bisa mendeteksi \r\n
				d = data.decode()
				rcv=rcv+d
				if rcv[-2:]=='\r\n':
					#end of command, proses string
					#logging.warning("data dari client: {}" . format(rcv))
					hasil = httpserver.proses(rcv)
					#hasil akan berupa bytes
					#untuk bisa ditambahi dengan string, maka string harus di encode
					hasil=hasil+"\r\n\r\n".encode()
					#logging.warning("balas ke  client: {}" . format(hasil))
					#hasil sudah dalam bentuk bytes
					connection.sendall(hasil)
					print('done sending')
					rcv=""
					connection.close()
					return
			else:
				break
		except OSError as e:
			pass
	connection.close()
	return



def Server():
	the_clients = []

	my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	my_socket.bind(('0.0.0.0', 8443))
	my_socket.listen(1)

	with ProcessPoolExecutor(20) as executor:
		while True:
			connection, client_address = my_socket.accept()
			try:
				#logging.warning("connection from {}".format(client_address))
				p = executor.submit(ProcessTheClient, connection, client_address)
				# the_clients.append(p)
			except ssl.SSLError as essl:
				print(str(essl))





def main():
	Server()

if __name__=="__main__":
	main()

