
# coding: utf-8

import cv2, glob, dlib

class DetectGender():

    def __init__(self):

        self.gender_list = ['Male', 'Female']

        self.detector = dlib.get_frontal_face_detector()

        self.gender_net = cv2.dnn.readNetFromCaffe(
                  'static/model/deploy_gender.prototxt',
                  'static/model/gender_net.caffemodel')
        self.gender = ""
        #이미지 경로(변경 필수)
        #self.img = glob.glob('static/img/capture.jpg')

    def detectowngender(self):
        img = cv2.imread('static/img/capture.jpg')

        faces = self.detector(img)

        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()

            face_img = img[y1:y2, x1:x2].copy()

            blob = cv2.dnn.blobFromImage(face_img, scalefactor=1, size=(227, 227),
            mean=(78.4263377603, 87.7689143744, 114.895847746),
            swapRB=False, crop=False)

        # predict gender
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = self.gender_list[gender_preds[0].argmax()]
        print(gender)
        self.gender = gender

    # #@main.route('/main', methods=['GET'])
    # def send_gender_to_html(self):
    #
    #     owngender={}
    #     owngender['gender']=self.detectowngender()
    #
    #     #print(owngender)
    #
    #     return render_template('/index.html', genderHtml=owngender)
