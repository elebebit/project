import sys
import os
import urllib
from PIL import Image

reload(sys)  
sys.setdefaultencoding('utf8')

def download(url, decode=False):
    response = urllib.urlopen(url)
    if response.geturl() == "https://s.yimg.com/pw/images/en-us/photo_unavailable.png":
        # Flickr :This photo is no longer available iamge.
        raise Exception("This photo is no longer available iamge.")

    body = response.read()
    if decode == True:
        body = body.decode()
    return body

def write(path, img):
    file = open(path, 'wb')
    file.write(img)
    file.close()
#001:bell 002:box 003:rake 004:stick
# see http://image-net.org/archive/words.txt
#classes = {"stick":"n04317833", "bell":"n03270695", "box":"n02971356", "rake":"n04050066"}
#classes = {"rake2":"n03417970"}
classes = {"stick2":"n04317420"}
offset = 0
max = 1500
for dir, id in classes.items():
    print(dir)
    os.makedirs(dir)
    urls = download("http://www.image-net.org/api/text/imagenet.synset.geturls?wnid="+id, decode=True).split()
    print(len(urls))
    i = 0
    for url in urls:
        if i < offset:
            continue
        if i > max:
            break

        try:
            file = os.path.split(url)[1]
            path = dir + "/" + file
            write(path, download(url))
            print("done:" + str(i) + ":" + file)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("error:" + str(i) + ":" + file)
        i = i + 1

print("end")
