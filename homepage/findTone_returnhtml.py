#!/usr/bin/env python
# coding: utf-8

import cv2,re,sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from xml.etree.ElementTree import parse
from PIL import Image
import random
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

class DetectTone:

    def __init__(self):
        # 입력 얼굴사진 지정하기
        self.image_file = "static/img/capture.jpg"
        self.yourtone=[]
        #plt.imshow(img)
        #plt.show()
        #self.parsehaircolor()
        #self.send_tone_to_html()

    def findFacetone(self,r,g,b):
        if r.isalpha or g.isalpha or b.isalpha:
            r=int(r)
            g=int(g)
            b=int(b)

        if r-g>=((g-b)*2.5):
            #print("cool")
            return "cool"
        else:
            #print("warm")
            return "warm"

    def detectowntone(self):
        # 입력 얼굴사진을 적절하게 변환하기
        img = mpimg.imread(self.image_file)
        # 출력 파일 이름
        output_file = re.sub(r'\.jpg|jpeg|PNG$', '-output.jpg', self.image_file)
        # 캐스케이드 파일의 경로 지정하기
        cascade_file = "static/xml/haarcascade_frontalface_alt.xml"
        # 이미지 읽어 들이기
        image = cv2.imread(self.image_file)
        # 그레이스케일로 변환하기
        image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 얼굴 인식 전용 캐스케이드 파일 읽어 들이기
        cascade = cv2.CascadeClassifier(cascade_file)
        # 얼굴 인식 실행하기
        # detectMultiScale - 얼굴 인식. minSize 이하의 크기는 무시. 너무 작게 지정하면 배경 등을 얼굴로 잘못 인식하게 된다.
        face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150))
        if len(face_list) == 1:
            # 인식한 부분 표시하기
            #print(face_list)
            color = (0, 0, 255)
            for face in face_list:
                x, y, w, h = face
                cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=1)
                #사각형 부분 자르기 아래의 출력 추가외는 관계없다
                #img_clone=img[y:y+h,x:x+w]
                y1=int(y+h*(1/2))
                x1=int(x+h*(1/2))
                h1=int(h*1/4)
                img_clone=img[y1-h1:y1+h1,x1-h1:x1+h1]
                #원래 파일에 사각형 출력 추가
                cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness=1)
            # 파일로 출력하기
            cv2.imwrite(output_file, image)
        else:
            print("no face or more face")
        #plt.imshow(img_clone)
        #plt.show()

        # 사진의 RGB 평균값 구하기
        Red = []
        Green = []
        Blue = []
        for x in img_clone:
            for y in x:
                Red.append(y[0])
                Green.append(y[1])
                Blue.append(y[2])
        R_max = max(Red)
        G_max = max(Green)
        B_max = max(Blue)
        R_avg = sum(Red) / len(Red)
        G_avg = sum(Green) / len(Green)
        B_avg = sum(Blue) / len(Blue)
        #print("Max Value")
        #print("R : ", R_max)
        #print("G : ", G_max)
        #print("B : ", B_max)
        #print("Avg Value")
        #print("R : ", R_avg)
        #print("G : ", G_avg)
        #print("B : ", B_avg)


        #비교 Y2552550 R25500 하여 거리기반으로 가까운 곳을 구한다
        #Y가 많으면 웜톤 R이많으면 쿨톤
        #여러사진을 비교한 결과 RGB에서 RG 평균값의 차이와 GB 평균값의 차이를 구해서 RG평균값 >= GB평균값*2.5이면 쿨톤이다

        if R_avg-G_avg>=((G_avg-B_avg)*2.5):
            #print("쿨톤")
            self.yourtone.append("쿨톤")
        else:
            #print("웜톤")
            self.yourtone.append("웜톤")


        #print(yourtone)
        #plt.imshow(img)
        #plt.show()

        reco_haircolor=self.parsehaircolor();
        return reco_haircolor,self.yourtone[0]

    #추천 머리색 추천

    def parsehaircolor(self):#머리색 xml파싱
        r=[]
        g=[]
        b=[]
        haircolor_Data=[]
        tree = parse('static/xml/color.xml')
        root = tree.getroot()
        color = root.findall("color")
        v_R = [x.findtext("r") for x in color]
        v_G = [x.findtext("g") for x in color]
        v_B = [x.findtext("b") for x in color]
        color_Name = [x.get("name") for x in root]
        haircolor_Data.append(color_Name)
        haircolor_Data.append(v_R)
        haircolor_Data.append(v_G)
        haircolor_Data.append(v_G)

        #파싱한 머리카락색의 톤을 구분해서 추가함
        haircolor_tone=[]
        for i in range(0,len(haircolor_Data[0])):
            temp=self.findFacetone(haircolor_Data[1][i],haircolor_Data[2][i],haircolor_Data[3][i])
            haircolor_tone.append(temp)
        haircolor_Data.append(haircolor_tone)
        haircolor_Data=[list(x) for x in zip(*haircolor_Data)]

        # haircolor_Data => 이름[i][0],R[i][1],G[i][2],B[i][3],톤구분[i][4](i는 순서)


        warmtone=[]
        cooltone=[]

        for tone in haircolor_Data:
            if(tone[4]=="cool"):
                cooltone.append(tone)
            else:
                warmtone.append(tone)

        #RGB 형식 변환 255,255,255 에서 FFFFFF으로
        for tone in cooltone:
            tone[1:4]=["#"+str(hex(int(tone[1])))[2:]+str(hex(int(tone[2])))[2:]+str(hex(int(tone[3])))[2:]]
            del tone[2]


        for tone in warmtone:
            tone[1:4]=["#"+str(hex(int(tone[1])))[2:]+str(hex(int(tone[2])))[2:]+str(hex(int(tone[3])))[2:]]
            del tone[2]

        #print(cooltone)
        #print(warmtone)

        if self.yourtone[0]=='쿨톤':
            reco_tone=random.sample(cooltone,5)
        else:
            reco_tone=random.sample(warmtone,5)

        #print(reco_tone)
        return reco_tone


    #@app.route("/", methods=['GET'])
    def send_tone_to_html(self):

        color,tone=self.detectowntone()
        print(color)
        print(tone)
        return render_template('/index.html', recocolorHtml=color, toneHtml=tone)
        #return render_template('index.html', recocolorHtml='color',toneHtml='tone')




tmp = DetectTone()
tmp.send_tone_to_html()


# In[267]:


#결과는 String으로 반환한다. flask로 딕셔너리 형태로 자바스크립트에 넘겨준다.
