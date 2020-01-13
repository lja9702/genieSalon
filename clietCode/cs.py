import socket
import time


'''
@author: k-young-passionate
@params:
    params: 보낼 image data 의 bytestream 
'''

def sendImage(params=b""):
  HOST, PORT = "211.254.215.243", 18070
  s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect((HOST, PORT)) 
  size = len(params)
  print(size)
  s.send(str(size).encode()) 
  time.sleep(0.1)
  s.send(params)
  s.close()
	
# TEST CODE
#f = open('./testimg.jpeg', 'rb')
#img = f.read()
#f.close()
#sendImage(img)
