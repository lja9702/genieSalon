
# coding: utf-8

# In[1]:


from PIL import Image
import glob
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

class MatchHair():
    def __inti__(self):
        
        print("")
        #print("init")
        
    def recoHairShape(self,shape,gender):
        
        root_path='static/img/hairShape'
        
        ownshape=shape["shape"]
        owngen=gender["gender"]
        
        if ownshape=='ang':
            images = glob.glob(root_path+'/' + owngen +'/' + ownshape + '/'+'*')
#             print(images)
#             for image_path in images:
#                 im = Image.open(image_path) # 이미지 불러오기
#                 #im.save('rename.jpeg') # 이미지 다른 이름으로 저장 
#                 im.show()
            
            return images
            
        elif ownshape=='egg':
            images = glob.glob(root_path+'/' + owngen +'/' + ownshape + '/'+'*')
            
            return images
            
        elif ownshape=='long':
            images = glob.glob(root_path+'/' + owngen +'/' + ownshape + '/'+'*')
            
            return images
            
            
        elif ownshape=='round':
            images = glob.glob(root_path+'/' + owngen +'/' + ownshape + '/'+'*')
            
            
            return images
            
            
    #@app.route("/", methods=['POST'])
    def send_recohair_to_html(self,shape,gender):
        hairpath=self.recoHairShape(shape,gender)
        
        recoHairPath={}
        
        for i in range(0,len(hairpath)):
            
            recoHairPath['reco_Hair_Path'+str(i+1)]=hairpath[i]
        
        print(recoHairPath)
        
        return render_template('/index.html', hairPathHtml=recoHairPath)
            

        
#아래와같은 모양과 성별을 받은뒤 머리모양 파일의 위치를 dict으로 알려준다.
shape={'shape' : "egg"}
gen={'gender' : "Man"}
go=MatchHair()
#go.recoHairShape(shape,gen)
go.send_recohair_to_html(shape,gen)

