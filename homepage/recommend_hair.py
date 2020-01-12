from PIL import Image
import glob
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

class MatchHair():
    def __init__(self):

        print("")
        #print("init")

    def recoHairShape(self,shape,gender):

        root_path='static/img/hairShape'

        if shape=='ang':
            images = glob.glob(root_path+'/' + gender +'/' + shape + '/'+'*')
#             print(images)
#             for image_path in images:
#                 im = Image.open(image_path) # 이미지 불러오기
#                 #im.save('rename.jpeg') # 이미지 다른 이름으로 저장
#                 im.show()

            return images

        elif shape=='egg':
            images = glob.glob(root_path+'/' + gender +'/' + shape + '/'+'*')

            return images

        elif shape=='long':
            images = glob.glob(root_path+'/' + gender +'/' + shape + '/'+'*')

            return images


        elif shape=='round':
            images = glob.glob(root_path+'/' + gender +'/' + shape + '/'+'*')


            return images

    def hairstyle_src_list(self, shape, gender):
        path=self.recoHairShape(shape,gender)

        hair_src_list = []

        for i in range(0,len(path)):

            hair_src_list.append(path[i])

        print(hair_src_list)
        return hair_src_list
    # #@app.route("/", methods=['POST'])
    # def send_recohair_to_html(self,shape,gender):
    #     hairpath=self.recoHairShape(shape,gender)
    #
    #     recoHairPath={}
    #
    #     for i in range(0,len(hairpath)):
    #
    #         recoHairPath['reco_Hair_Path'+str(i+1)]=hairpath[i]
    #
    #     print(recoHairPath)
    #
    #     return render_template('/index.html', hairPathHtml=recoHairPath)
    #

#
# #아래와같은 모양과 성별을 받은뒤 머리모양 파일의 위치를 dict으로 알려준다.
# shape={'shape' : "egg"}
# gen={'gender' : "Male"}
# go=MatchHair()
# #go.recoHairShape(shape,gen)
# go.hairstyle_src_list(shape,gen)
