import requests


def getRequest(addUrl="", params="", conType="GET"):
  URL = 'http://211.254.215.243:18070/' + addUrl

#f = open('./cpimg.jpeg', 'rb')
#img = f.read()
#f.close()
#params = {'hi' : 'hi2', 'hello': img}

  if conType == "GET":
    res = requests.get(URL, data=params)
  elif conType == "POST":
    res = requests.post(URL, data=params)
  else:
    return (404, "Page not found")

  return (res.status_code, res.text)


# TEST CODE
# c = {'hi' : 'asdf'}
# print(getRequest('ih', c, "POST"))
