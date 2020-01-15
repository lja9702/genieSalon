import socket
import sys
import threading
import time
import re
import json
from urllib import parse
import random
import os

recentip = {}
blockedip = []
BFSIZE = 4096
imgindex = -1

faceshapes = {"ang":"각진 얼굴", "egg":"계란형 얼굴", "round":"둥근형 얼굴", "long":"긴 얼굴", "tri":"역삼각형 얼굴"}


def readIndex(flag=False):
	imginfile = open("./pimg/index.txt", "r")
	imgindex = int(imginfile.read())
	imginfile.close()
	if flag:
		imginfile = open("./pimg/index.txt", "w")
		imgindex += 1
		imginfile.write(str(imgindex))
		imginfile.close()
	return imgindex


def tcpHandler(clientSocket, addr):
	global recentip, blockedip, BFSIZE, imgindex

	tmp = clientSocket.recv(BFSIZE)
	print(tmp)
	try:
		size = int(tmp)
		cnt = int(size / BFSIZE)
		if size % BFSIZE != 0:
			cnt += 1
#		cnt += 1
		tmp = b''
		size = 0
		for i in range(cnt):
			time.sleep(0.1)
			ttmp = clientSocket.recv(BFSIZE)
			size += len(ttmp)
			tmp += ttmp
			print(i, cnt, len(ttmp))
		print("size: " + str(size))
		imgindex = readIndex(True)
		wf = open("./pimg/capture" + str(imgindex) + ".jpg", "wb")
		wf.write(tmp)
		wf.close()
		header = "HTTP/1.1 200 OK\r\n"
		res = "SUCCESS"
		clientSocket.sendall((header+res).encode())
		clientSocket.close()

		return

	except:
		print("except")



if __name__ == "__main__":
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, BFSIZE)
	host = socket.gethostbyname(socket.gethostname())
	tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSocket.bind(("0.0.0.0", int(sys.argv[1])))
	tcpSocket.listen(100)

	while True:
		(cSocket, addr) = tcpSocket.accept()
		tcpThread = threading.Thread(target=tcpHandler, args=(cSocket,addr ))
		tcpThread.start()

	tcpSocket.close()
