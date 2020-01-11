from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import imutils
import cv2
import random, glob, os
from detect_shape import DetectShape
from detect_gender import DetectGender
from find_tone import DetectTone
from recommend_hair import MatchHair

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()

# initialize a flask object
app = Flask(__name__)

vs = VideoStream(src=0).start()
#time.sleep(2.0)

#얼굴 인식 캐스케이드 파일 읽는다
face_cascade = cv2.CascadeClassifier('static/xml/haarcascade_frontface.xml')
detect_shape = DetectShape()
detect_gender = DetectGender()

stop_record = False	#동영상 출력 종료 여부 변수
@app.route("/findSalon")
def findsalon_page():
	return render_template("findSalon.html")

@app.route("/main")
def main_page():
	return render_template("main.html")

@app.route("/camera")
def camera_page():
	return render_template("camera.html")

@app.route("/recommendation")
def camtorecommed_page():
	#셀럽 이름과 이미지 경로
	celeb_src , celeb_name = find_celeb()
	#컬러 추천과 cool톤에 해당되는 percent 출력
	find_tone = DetectTone()
	color_list, cool = find_tone.detectowntone()
	warm = str(100 - int(cool))
	#헤어스타일 추천
	match_hair = MatchHair()
	print("shape: %s gender: %s" %(detect_shape.shape, detect_gender.gender))
	hair_list = match_hair.hairstyle_src_list(shape = detect_shape.shape, gender = detect_gender.gender)
	return render_template("recommendation.html", celebSrc = celeb_src, celebName = celeb_name,
	colorList = color_list, cool = cool, warm = warm, hairList = hair_list)

'''camera에서 얼굴을 인식해서 recommendation.html로 redirect를 하기위해 값을 넘기는 함수'''
@app.route("/camera/isFinished")
def is_finished():
	return str(stop_record)

count = 0
def check_count():
	global count
	if(count == 60):
		return
	count += 1
	print("count: %d" %count)

def find_celeb():
	global detect_shape, detect_gender
	shape = detect_shape.shape
	gender = detect_gender.gender

	print("shape: %s gender: %s" %(shape, gender))

	img_path = "static/img/celeb/" + gender + "/" + shape
	print("img_path: %s" %img_path)
	#특정 얼굴형 젠더에서 랜덤으로 사진 가져오기
	file = random.choice([
    x for x in os.listdir(img_path)
    if os.path.isfile(os.path.join(img_path, x)) and
    x.endswith('.jpg')])

	celeb_src = img_path + "/" + file

	return [celeb_src, file[:-4]]

def detect_face():
	# grab global references to the video stream, output frame, and
	# lock variables
	global vs, outputFrame, lock, stop_record, count, detect_shape

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#얼굴 인식
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
		#인식된 얼굴 갯수 출력
		print(len(faces))
		#얼굴이 1개 인식되면
		if(len(faces) == 1):
			#얼굴이 인식되면 타이머를 통하여 5초 후 사진이 찍히도록 thread를 시작한다
			timer = threading.Timer(1, check_count)
			timer.start()
			#5초뒤 timer를 종료하고 다른 웹으로 넘어가게한다.
			if count == 60:
				print('stop')
				timer.cancel()
				cv2.imwrite("static/img/capture.jpg",frame) #save image
				#얼굴형 판정, 성별 판정
				detect_shape.measure_face_shape()
				detect_gender.detectowngender()

				stop_record = True
				break

			for (x,y,w,h) in faces:
				cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

		# acquire the lock, set the output frame, and release the
		# lock
		with lock:
			outputFrame = frame.copy()

def generate(face_detect_func):
	# grab global references to the output frame and lock variables
	global outputFrame, lock, stop_record

	# start a thread that will perform motion detection
	t = threading.Thread(target=face_detect_func)
	t.daemon = True
	t.start()

	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if stop_record is True:
				print("redirect camtorecommed page")
				# release the video stream pointer
				vs.stop()
				break

			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
			bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(detect_face),
		mimetype = "multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())

	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)

'''
https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/
'''
