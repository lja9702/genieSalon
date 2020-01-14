from cs import sendImage

f = open('./testimg.jpeg', 'rb')
img = f.read()
f.close()
print(len(img))
sendImage(img)
