import sys
import os
import dlib
import glob
import cv2  #opencv 사용

'''
camera 영상을 보여주는 함수
'''
def showVideoRGB():
    cap=cv2.VideoCapture(0)
    print("width:%d, height: %d" %(cap.get(3), cap.get(4)))

    while(True):
        ret, frame=cap.read()
        cv2.imshow('frame_color', frame)  # 컬러 화면 출력
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


'''
RGB > BGR or BGR > RGB 변환
dlib는 RGB 형태로 이미지를 사용하고
openCV는 BGR 형태이므로 B와 R을 바꿔주는 함수가 필요하다.
'''
def swapRGB2BGR(img):
    r, g, b = cv2.split(img)
    bgr = cv2.merge([b,g,r])
    return bgr

'''랜드마크 포인트를 리턴하는 함수'''
def find_landmark_point():
    #opencv에서 ESC 키입력 상수
    #ESC_KEY = 27

    # 랜드마크 파일 경로
    predictor_path = sys.argv[1]
    # 이미지 경로
    faces_folder_path = sys.argv[2]

    # 얼굴 인식용 클래스 생성 (기본 제공되는 얼굴 인식 모델 사용)
    detector = dlib.get_frontal_face_detector()
    # 인식된 얼굴에서 랜드마크 찾기위한 클래스 생성
    predictor = dlib.shape_predictor(predictor_path)

    # 이미지를 화면에 표시하기 위한 openCV 윈도 생성
    #cv2.namedWindow('Face')
    img = cv2.imread(faces_folder_path + "capture.jpg", cv2.IMREAD_ANYCOLOR)

    #이미지를 두배로 키운다.
    cvImg = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)

    # 얼굴 인식 두번째 변수 1은 업샘플링을 한번 하겠다는 얘기인데
    # 업샘플링을하면 더 많이 인식할 수 있다고 한다.
    # 다만 값이 커질수록 느리고 메모리도 많이 잡아먹는다.
    # 그냥 1이면 될 듯.
    dets = detector(img, 1)

    # 인식된 얼굴 개수 출력
    print("Number of faces detected: {}".format(len(dets)))

    '''랜드마크 포인트 리스트'''
    pointlist = []
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
            pointlist.append((x, y))
            # 이미지 랜드마크 좌표 지점에 인덱스(랜드마크번호, 여기선 i)를 putText로 표시해준다.
            #cv2.putText(cvImg, str(i), (x, y), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.3, (0, 255, 0))
        # 랜드마크가 표시된 이미지를 openCV 윈도에 표시
        #cv2.imshow('Face', cvImg)

    # 무한 대기를 타고 있다가 ESC 키가 눌리면 빠져나와 다음 이미지를 검색한다.
    # while True:
    #     if cv2.waitKey(0) == ESC_KEY:
    #         break;
    # cv2.destroyWindow('Face')
    for (x, y) in pointlist:
        print("x: %d y: %d" %(x, y))

#def measure_face_shape(pointlist):

find_landmark_point()
