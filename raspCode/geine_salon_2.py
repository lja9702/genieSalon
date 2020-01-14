#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 1: GiGA Genie Keyword Spotting"""

from __future__ import print_function
from time import sleep

import client_conn
import picamera
import grpc
import audioop
from ctypes import *
import RPi.GPIO as GPIO
import ktkws # KWS
import MicrophoneStream as MS
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import user_auth as UA
import os
import webbrowser
import subprocess
import threading


KWSID = ['기가지니', '지니야', '친구야', '자기야']
HOST = 'gate.gigagenie.ai'
PORT = 4080
RATE = 16000
CHUNK = 512

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
btn_status = False

def callback(channel):  
	print("falling edge detected from pin {}".format(channel))
	global btn_status
	btn_status = True
	print(btn_status)

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)


def detect():
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:

			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))

			if (rc == 1):
				print("detect")
				MS.play_file("../data/sample_sound.wav")
				return 200

def btn_detect():
	global btn_status
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:
			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			GPIO.output(31, GPIO.LOW)
			if (btn_status == True):
				rc = 1
				btn_status = False			
			if (rc == 1):
				GPIO.output(31, GPIO.HIGH)
				MS.play_file("../data/sample_sound.wav")
				return 200

def device_awake_speech(key_word = '기가지니'):
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n호출어를 불러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc

def device_awake_btn(key_word = '기가지니'):
	global btn_status
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	print ('start rc = %d' % (rc))
	print ('\n버튼을 눌러보세요~\n')
	ktkws.set_keyword(KWSID.index(key_word))
	rc = btn_detect()
	print ('detect rc = %d' % (rc))
	print ('\n\n호출어가 정상적으로 인식되었습니다.\n\n')
	ktkws.stop()
	return rc


def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
    
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message
            
            rms = audioop.rms(content,2)
            #print_rms(rms)

def getVoice2Text():	
    print ("\n\n음성인식을 시작합니다.\n\n종료하시려면 Ctrl+\ 키를 누루세요.\n\n\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request()
    resultText = ''
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200: # partial
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            resultText = response.recognizedText
            break
        else:
            print('resultCd=%d | recognizedText= %s' 
                  % (response.resultCd, response.recognizedText))
            break

    print ("\n\n인식결과: %s \n\n\n" % (resultText))
    return resultText


# TTS : getText2VoiceUrl
def getText2VoiceUrl(inText):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	response = stub.getText2VoiceUrl(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("TTS 생성에 성공하였습니다.\n\n\n아래 URL을 웹브라우져에 넣어보세요.")
		print ("Stream Url: %s\n\n" % (response.url))
	else:
		print ("TTS 생성에 실패하였습니다.")
		print ("Fail: %d" % (response.resultCd)) 

# TTS : getText2VoiceStream
def getText2VoiceStream(inText,inFileName):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	writeFile=open(inFileName,'wb')
	for response in stub.getText2VoiceStream(message):
		if response.HasField("resOptions"):
			print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	return response.resOptions.resultCd


def openbrowser(url):
    webbrowser.open(url,new=0,autoraise= False)
    

lock = threading.Lock()
isOpenWeb = False
isRecomm_url = 0

def gigagenie_talk():
    global lock, isOpenWeb
    
    device_awake_speech()
    text = getVoice2Text()
    
    while text.find("미용실")==-1:
        device_awake_speech()
        text = getVoice2Text()
        #getText2VoiceStream("지니살롱에 오신것을 환영합니다. 추천을 받으시려면 사진찍어줘를 말해주세요.", output_file)
        #MS.play_file(output_file)
    if(text.find("지니 살롱") != -1 or text.find("미용실") != -1):
        print("goto geniesalon")
        isOpenWeb = True
    
        while(isOpenWeb is True):
            print("url open!!")
            sleep(1)
        
        device_awake_speech()
        text = getVoice2Text()
        
    while text.find("사진") == -1 and text.find("주변") == -1 and text.find("근처") ==-1:
            device_awake_speech()
            text=getVoice2Text()
            print(text)
    
    print("check keyword picture or gucnhar")
    if text.find("사진") != -1:
        getText2VoiceStream("네. 준비가되시면 지니야를 불러주세요.", output_file)
        MS.play_file(output_file)
        #take a picture
        camera.start_preview()
        text = getVoice2Text()
        while text.find("지니") ==-1:
            text=getVoice2Text()
        camera.capture(img_src)
        camera.stop_preview()
        #send picture to server
        print("start send img")
        img_send=open(img_src,"rb")
        img_tmp = img_send.read()
        img_send.close()
        client_conn.sendImage(img_tmp)
        print("send img")
        sleep(5)
        getText2VoiceStream("사진이 전송되는동안 잠시 기다려주세요", output_file)
        MS.play_file(output_file)
        
        isRecomm_url = 1
        isOpenWeb = True
        
        while(isOpenWeb is True):
            print("url open!~")
            sleep(1)
            
        device_awake_speech()
        text = getVoice2Text()
    
    elif text.find("주변") != -1 or text.find("근처") != -1: #'주변' or '근처' 미용실정보 
        print("jubyeon")
        #getText2VoiceStream("주변 미용실정보를 보여드릴께요", output_file)
        #MS.play_file(output_file)
        isRecomm_url = 2
        isOpenWeb = True
        
        while(isOpenWeb is True):
            print("url open!~!!!!!!!!!!!!!1")
            sleep(1)
            
        device_awake_speech()
        text = getVoice2Text()
    
                    
def main():
        
        global lock, isOpenWeb, isRecomm_url
        #setting env
        img_src = '/home/pi/ai-makers-kit/python3/genieSalon/homepage/static/img/capture.jpg'
        url = 'http://211.254.215.243:18070'
        output_file = "testtts.wav"
        camera = picamera.PiCamera()
        camera.resolution=(720,480)
        t=threading.Thread(target=gigagenie_talk)
        t.daemon = True
        t.start()
        #check word to open app
        
        while(isOpenWeb is False):
            print("Not open url")
            sleep(1)
        
        webbrowser.open(url)
        isOpenWeb = False
        
 
        while(isOpenWeb is False):
            print("locking befor recomm")
            sleep(1)
            
        if(isRecomm_url == 1):
            webbrowser.open(url + "/recommendation")
    
        elif(isRecomm_url == 2):
            findsalon_url=(url + '/findSalon')
            
        ifOpenWeb = False
            #webbrowser.open("http://211.254.215.243:18070/findSalon")
            
        text = getVoice2Text()
        while text.find("예약") == -1:
            text=getVoice2Text()
            
        print("ok.goto reservation")
            
                
                
                
                
                
        
       
	
	
	
	

if __name__ == '__main__':
	main()

