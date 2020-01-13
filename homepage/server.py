import socket
import sys
import threading
import time
import re
import json
from urllib import parse

recentip = {}
blockedip = []

def tcpHandler(clientSocket, addr):
	global recentip, blockedip
	
#	tmp = clientSocket.recv(4096)
	tmp = b'' 
	size = 0
	while True:
#		tmp = clientSocket.recvall()
		ttmp = clientSocket.recv(4096)
#		print("ssss")
#		print(len(ttmp))
#		print("eeee")
		size += len(ttmp)
		tmp += ttmp

		if len(ttmp) < 4096:
			print("size: " + str(size))
			break

	req_in = tmp.decode("utf-8")

	if addr[0] in blockedip:
		return
	'''
	try:
		recentip[addr[0]] += 1
	except:
		recentip[addr[0]] = 1
	'''
	print(recentip)
	print(req_in)
	print()
	print()
	print()

	if req_in[:3] == "GET":
		req_in = req_in.split("GET")
		req_in = req_in[1].split()
		f = req_in[0][1:]
		f = parse.unquote(f)
		getHandler(f, clientSocket)
	elif req_in[:4] == "POST":
		dataIndex = 0
		req_in = req_in.split('\r\n')
		for i in range(len(req_in)):
			if req_in[i] == '':
				dataIndex = i+1
				break
		f = req_in[0].split()[1] 
		f = parse.unquote(f)
		data = req_in[dataIndex]
#		data = parse.unquote(data)
		postHandler(f[1:], data, clientSocket)
#	clientSocket.close()

def postHandler(f, data, clientSocket):

	print("post")
	print(f)
	print(data)
	if f != "upload":
		data = parse.unquote(data)
	data = data.split("&")
	datas = {}
	for d in data:
		tmp_d = d.split("=", 1)
		datas[tmp_d[0]] = tmp_d[1]

	if f == "reservation":
		rarray = []
		rf = open("./db/db.txt", "r")
		read = rf.read()
		rf.close()
		read = read.split("\n")
		for r in read:
			tmp = {}
			r = r.split('\t')
			print(r)
			try:
				for _r in r:
					rr = _r.split("=")
					tmp[rr[0]] = rr[1]
				rarray.append(tmp.copy())
			except:
				pass
		
		
		s, n, d, t, p = datas["salon"], datas["name"], datas["day"], datas["time"], datas["phone"]

		sucFile = open("./templates/result_success.html", "rb")
		res = sucFile.read()
		sucFile.close()
		header = "HTTP/1.1 200 OK\r\n"
		flag = True
		for i in rarray:
			if i["day"] == d and i["time"] == t:
				if i["phone"] == p:
					failFile = open("./templates/result_fail.html", "rb")
					res = failFile.read()
					failFile.close()
					header = "HTTP/1.1 500 ERROR OCCURED\r\n"
					flag = False
				elif i["salon"] == s:
					failFile = open("./templates/result_fail.html", "rb")
					res = failFile.read()
					header = "HTTP/1.1 500 ERROR OCCURED\r\n"
					failFile.close()
					flag = False

		if flag:
			wf = open("./db/db.txt", "a")
			towrite = "salon="+s + "\tname=" + n + "\tday=" + d + "\ttime=" + t + "\tphone=" + p + "\n"
			wf.write(towrite)
			wf.close()
	elif f == "upload":
#	try:
		wf = open("./pimg/" + datas["hi"], "wb")
		wf.write(datas["capture"])
		wf.close()
		header = "HTTP/1.1 200 OK\r\n"
		res = "SUCCESS"
#		except:
#			header = "HTTP/1.1 500 ERROR OCCURED\r\n"
#			res = "NO"

	header += "Keep-Alive: timeout=10, max=100\r\n" #timeout=10, max=100\r\n"
	header += "Connection: keep-alive\r\n"
	header += "Content-Type: text/html\r\n"
	header += "Content-Length: "+str(len(res))+"\r\n"
	header += "\r\n"
	header = header.encode('utf-8')
	res = header + res.encode('utf-8')
	print('post')
#	print(res)
	clientSocket.sendall(res)
	return 	
	
	
def getHandler(f, clientSocket):

	if f == "":
		f = "main.html"
	if f == "my_json":
		ff = open("./static/img/favicon.ico", 'rb')
		fi = ff.read()
		ff.close()
		j = json.dumps({'foo':'my json', 'a':fi.decode('utf-8')})
		header = "HTTP/1.1 200 OK\r\n"
		header += "Keep-Alive: timeout=10, max=100\r\n" #timeout=10, max=100\r\n"
		header += "Connection: keep-alive\r\n"
		header += "Content-Type: application/json\r\n"
		header += "\r\n"
		res = header + j
		clientSocket.sendall(res.encode('utf-8'))
		return


	
	p = ""
	header = "HTTP/1.1 200 OK\r\n"
	header += "Keep-Alive: timeout=10, max=100\r\n" #timeout=10, max=100\r\n"
	header += "Connection: keep-alive\r\n"

	if '.' not in f:
		if f != "reservation":
			f += ".html"
	if '?' in f:
		f = f.split("?")
		p = f[1]
		f = f[0]
		p = p.split("&")

	if re.search('.html', f, re.IGNORECASE):
		f = "./templates/" + f
		mimetype = "text/html"
	elif re.search('.xml', f, re.IGNORECASE):		
#		f = "./static/xml/" + f
		mimetype = "text/xml"
	elif re.search('.css', f, re.IGNORECASE):
#		f = "./static/css/" + f
		mimetype = "text/css"
	elif re.search('.js', f, re.IGNORECASE):
#		f = "./static/js/" + f
		mimetype = "text/javascript"
	elif re.search('.jpg', f, re.IGNORECASE):		
#		f = "./statc/resource/" + f
		mimetype = "image/jpg"
	elif re.search('.jpeg', f, re.IGNORECASE):		
#		f = "./static/resource/" + f
		mimetype = "image/jpeg"
	elif re.search('.png', f, re.IGNORECASE):		
#		f = "./static/resource/" + f
		mimetype = "image/png"
		header += "Content-Type: image/png\r\n"
	elif re.search('mp4', f, re.IGNORECASE):
#		f = "./static/resource/" + f
		mimetype = "video/mp4"
	elif re.search('.ico', f, re.IGNORECASE):
		f = "./static/img/" + f
		mimetype = "image/vnd.microsoft.icon"
	else:
#		f = "./static/resource/" + f
		mimetype = "Application/octet-stream"

	try:
		rf = open(f, "rb")
	except:
		header = "HTTP/1.1 404 NOT FOUND\r\n"
		print(f + " is not found.")
		clientSocket.sendall(header.encode('utf-8'))
		return
		

	res = rf.read()
	if len(p) > 1 or (len(p) == 1 and p != ""):
		res = res.decode('utf-8')
		res = res.replace("지니살롱", p[0])
		res = res.encode('utf-8')
	header += "Content-Length: "+str(len(res))+"\r\n"
	header += "Content-Type: " + mimetype + "\r\n"
	header += "\r\n"

	res = header.encode("utf-8") + res
	clientSocket.sendall(res)
	rf.close()

def dosHandler():
	global recentip, blockedip
	while True:
		time.sleep(10)

		for i in recentip:
			if recentip[i] >= 18:
				blockedip.append(i)
			else:
				recentip[i] = 0
	

if __name__ == "__main__":
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = socket.gethostbyname(socket.gethostname())
#	tcpSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
	tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpSocket.bind(("0.0.0.0", int(sys.argv[1])))
	tcpSocket.listen(100)

	dosThread = threading.Thread(target=dosHandler, args=())
	dosThread.start()
	while True:
		(cSocket, addr) = tcpSocket.accept()
		tcpThread = threading.Thread(target=tcpHandler, args=(cSocket,addr ))
		tcpThread.start()

	tcpSocket.close()
