import sys
import os
import dlib
import glob
import cv2  #opencv 사용
import math
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

class DetectShape:
    #opencv에서 ESC 키입력 상수
    #ESC_KEY = 27
    def __init__(self):
        # 랜드마크 파일 경로
        self.predictor_path = "static/model/shape_predictor_68_face_landmarks.dat"
        # 이미지 경로
        self.img_path = "static/img/capture.jpg"
        #랜드마크 포인트 리스트
        self.landmark_list = []
        self.shape = ""

    '''랜드마크 포인트를 찾는 함수'''
    def find_landmark_point(self):

        # 얼굴 인식용 클래스 생성 (기본 제공되는 얼굴 인식 모델 사용)
        detector = dlib.get_frontal_face_detector()
        # 인식된 얼굴에서 랜드마크 찾기위한 클래스 생성
        predictor = dlib.shape_predictor(self.predictor_path)

        # 이미지를 화면에 표시하기 위한 openCV 윈도 생성
        #cv2.namedWindow('Face')
        img = cv2.imread(self.img_path, cv2.IMREAD_ANYCOLOR)

        #이미지를 두배로 키운다.
        cvImg = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)

        # 얼굴 인식 두번째 변수 1은 업샘플링을 한번 하겠다는 얘기인데
        # 업샘플링을하면 더 많이 인식할 수 있다고 한다.
        # 다만 값이 커질수록 느리고 메모리도 많이 잡아먹는다.
        # 그냥 1이면 될 듯.
        dets = detector(img, 1)

        # 인식된 얼굴 개수 출력
        print("Number of faces detected: {}".format(len(dets)))

        # 이제부터 인식된 얼굴 개수만큼 반복하여 얼굴 윤곽을 표시할 것이다.
        for k, d in enumerate(dets):
            # k 얼굴 인덱스
            # d 얼굴 좌표
            print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
                k, d.left(), d.top(), d.right(), d.bottom()))

            # 인식된 좌표에서 랜드마크 추출
            shape = predictor(img, d)
            print(shape.num_parts)
            # num_parts(랜드마크 구조체)를 하나씩 루프를 돌린다.
            for i in range(0, shape.num_parts):
                # 해당 X,Y 좌표를 두배로 키워 좌표를 얻고
                x = shape.part(i).x*2
                y = shape.part(i).y*2

                # 좌표값 출력
                print(str(x) + " " + str(y))
                self.landmark_list.append((x, y))
                # 이미지 랜드마크 좌표 지점에 인덱스(랜드마크번호, 여기선 i)를 putText로 표시해준다.
                #cv2.putText(cvImg, str(i), (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.3, (0, 255, 0))
            # 랜드마크가 표시된 이미지를 openCV 윈도에 표시
            #cv2.imshow('Face', cvImg)

        # 무한 대기를 타고 있다가 ESC 키가 눌리면 빠져나와 다음 이미지를 검색한다.
        # while True:
        #     if cv2.waitKey(0) == ESC_KEY:
        #         break;
        # cv2.destroyWindow('Face')
        for (x, y) in self.landmark_list:
            print("x: %d y: %d" %(x, y))


    '''
    얼굴형을 측정하고 얼굴형에 해당하는 문자열 반환
    #upper_width: 2번과 14번 랜드마크 길이
    #lower_width: 5번과 11번의 랜드마크 길이
    #eyebrow_to_chin: 27번과 8번 랜드마크 길이 (미간부터 턱까지 길이)
    #height: eyebrow_to_chin + eyebrow_to_chin / 3
    '''
    def measure_face_shape(self):

        self.find_landmark_point()

        upper_width = math.sqrt(pow(self.landmark_list[2][0] - self.landmark_list[14][0], 2) \
        + pow(self.landmark_list[2][1] - self.landmark_list[14][1], 2))

        lower_width = math.sqrt(pow(self.landmark_list[5][0] - self.landmark_list[11][0], 2) \
        + pow(self.landmark_list[5][1] - self.landmark_list[11][1], 2))

        eyebrow_to_chin = math.sqrt(pow(self.landmark_list[27][0] - self.landmark_list[8][0], 2) \
        + pow(self.landmark_list[27][1] - self.landmark_list[8][1], 2))

        height = eyebrow_to_chin + eyebrow_to_chin / 3
        rate = height / upper_width
        print("upper: %lf lower: %lf height: %lf rate: %lf" %(upper_width, lower_width, height, rate))

        #각진 얼굴
        print("upper_width / lower_width: %lf" %(upper_width / lower_width))
        if upper_width / lower_width < 1.4:
            self.shape = "ang"
        #게란형 얼굴
        elif (rate > 1.11 and rate < 1.5):
            self.shape = "egg"
        #둥근형 얼굴
        elif rate <= 1.11:
            self.shape = "round"
        #긴 얼굴
        elif rate >= 1.5:
            self.shape = "long"
        #역삼각형 얼굴
        else:
            self.shape = "tri"
