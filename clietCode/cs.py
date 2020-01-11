import requests


'''
@author: k-young-passionate
@params:
		addUrl: url 뒤에 추가할 경로
		params: 서버에 body에 넣어 보낼 값 map 으로 전달
		conType: GET 방식과 POST 방식 구분, default는 GET
@return:  (response code, response message) 
'''

def getRequest(addUrl="", params="", conType="GET"):
  URL = 'http://211.254.215.243:18070/' + addUrl

  if conType == "GET":
    res = requests.get(URL, data=params)
  elif conType == "POST":
    res = requests.post(URL, data=params)
  else:
    return (404, "Page not found")

  return (res.status_code, res.text)


# TEST CODE
# c = {'hi' : 'asdf'}
# f = open('./test.jpeg', 'rb')
# img = f.read()
# f.close()
# params = {'hi' : 'hi2', 'hello': img}
# print(getRequest('ih', c, "POST"))
