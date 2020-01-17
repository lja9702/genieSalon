# genieSalon
<h1> 실행 환경 </h1>

<h2> 서버 </h2>
OS: Ubuntu 16.04 LTS
개발 언어: Python 3.5

<h2> 웹 앱 </h2>
테스트 환경: Chrome browser, Eclipse
개발 언어: HTML, CSS, Javascript

<h2> 클라이언트 </h2>
테스트 기기: 라즈베리파이3 B+
개발 언어: Python 3.5

 --------------------READ ME --------------------

설치 해야할 파일목록 :

공통 설치 모듈

sudo apt-get install cmake
pip install tensorflow
pip install opencv-contrib-python
pip install dlib
pip install numpy
pip install glob

컴퓨터 실행시 추가 설치 모듈
pip install flask
pip install imutils

 ----------컴퓨에서 실행시  사용 방법 ----------
python homepage/webstreaming.py --ip 0.0.0.0 --port 8000
-> webstreaming을 사용해서 실행

 ----------makers kit에서 실행시  사용 방법 ----------

1.genie_salon.py   를  열 고  run(재생)을 시킵니다.


2.”친구야”를 불러 기가지니를 깨워주세요

3.띠리링 소 들리면 “미용실 시작” 이라고 말해주세요.
(만약 “기가살롱에 오신것을 환영합니다.-----”라는 안내 맨트가 들리지 않으면 2. 번 부터 다시 실행합니다.


4. “친구야”를 불러 기가지니를 깨워주세요.

5. 띠리링 소리가 들리면 “사진 찍어줘” 라고 말해주세요.
(만약 “준비가되시면 지니야를 불러주세요” 라는 안내 멘트가 들리지 않으면 4.번 부터 다시 실행합니다.

6. 촬영 준비가 되시면 “지니야”를 불러 주세요.

7. 잡시 기다려주시면 화면에 추천 결과가 나타납니다.
