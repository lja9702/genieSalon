import cv2,re,sys,dlib
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

        self.detector = dlib.get_frontal_face_detector()

        self.yourtone = {}
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

        img = cv2.imread(self.image_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #plt.imshow(img)
        #plt.show()

        faces = self.detector(img)
        #print(faces)

        # 인식한 부분 표시하기
        #print(face_list)

        # 인식할 얼굴이 없음
        if len(faces) == 0:
            print("no face")
            return

        for face in faces:


            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()


            img_clone = img[y1:y2, x1+int(1/4*(x2-x1)):x2-int(1/4*(x2-x1))].copy()
#             plt.imshow(img_clone)
#             plt.show()
#             x, y, w, h = face
#             cv2.rectangle(image, (x, y), (x+w, y+h), color, thickness=1)
#             #사각형 부분 자르기 아래의 출력 추가외는 관계없다
#             #img_clone=img[y:y+h,x:x+w]
#             y1=int(y+h*(1/2))
#             x1=int(x+h*(1/2))
#             h1=int(h*1/4)
#             img_clone=img[y1-h1:y1+h1,x1-h1:x1+h1]
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
#         print("Max Value")
#         print("R : ", R_max)
#         print("G : ", G_max)
#         print("B : ", B_max)
#         print("Avg Value")
#         print("R : ", R_avg)
#         print("G : ", G_avg)
#         print("B : ", B_avg)


        #비교 Y2552550 R25500 하여 거리기반으로 가까운 곳을 구한다
        #Y가 많으면 웜톤 R이많으면 쿨톤
        #여러사진을 비교한 결과 RGB에서 RG 평균값의 차이와 GB 평균값의 차이를 구해서 RG평균값 >= GB평균값*2.5이면 쿨톤이다

        if R_avg-G_avg>=((G_avg-B_avg)*2.5):
            temp = G_avg<B_avg and 100 or 100-(G_avg-B_avg)/(R_avg-B_avg)*100
            #print("쿨톤")
        else:
            temp = G_avg>R_avg and 100 or 50-(G_avg-B_avg)/(R_avg-B_avg)*100
            #print("웜톤")
        self.yourtone['cool']=round(temp, 2) # 소수점 둘째자리까지만


        #print(yourtone)
        #plt.imshow(img)
        #plt.show()

        reco_haircolor=self.parsehaircolor();
#         a={}
#         b={}
#         for i in range(0,len(reco_haircolor)):
#             print(i)
#             a['reco_colo_name'+str(i+1)]=reco_haircolor[i][0]
#             b['reco_colo_value'+str(i+1)]=reco_haircolor[i][1]

#         print(a)

        return reco_haircolor,self.yourtone['cool']

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
            r_hex = str(hex(int(tone[1])))[2:]
            if len(r_hex) < 2:
                r_hex = "0" + r_hex
            g_hex = str(hex(int(tone[2])))[2:]
            b_hex = str(hex(int(tone[3])))[2:]

            tone[1:4]=["#"+r_hex+g_hex+b_hex]

            del tone[2]


        for tone in warmtone:
            r_hex = str(hex(int(tone[1])))[2:]
            if len(r_hex) < 2:
                r_hex = "0" + r_hex
            g_hex = str(hex(int(tone[2])))[2:]
            b_hex = str(hex(int(tone[3])))[2:]

            tone[1:4]=["#"+r_hex+g_hex+b_hex]

            del tone[2]

        #print(cooltone)
        #print(warmtone)
        '''cool톤의 비율이 50%를 넘을 경우'''
        if self.yourtone['cool'] > 50:
            reco_tone=random.sample(cooltone,5)
        else:
            reco_tone=random.sample(warmtone,5)

        #print(reco_tone)
        return reco_tone





    #@app.route("/", methods=['GET'])
#     def send_tone_to_html(self):
#
#         color,tone=self.detectowntone()
#         recoColorName={}
#         recoColorValue={}
#         for i in range(0,len(color)):
#
#             recoColorName['reco_colo_name'+str(i+1)]=color[i][0]
#             recoColorValue['reco_colo_value'+str(i+1)]=color[i][1]
#percent
# #         print(tone)
# #         print(recoColorName)
# #         print(recoColorValue)
#         return render_template('/index.html',recoColorValueHtml=recoColorValue, recoColorNameHtml=recoColorName, toneHtml=tone)
#


#todo=DetectTone()
#print(todo.detectowntone())
# print(todo.send_tone_to_html())
#todo.detectowntone()

#결과는 String으로 반환한다. flask로 딕셔너리 형태로 자바스크립트에 넘겨준다.
