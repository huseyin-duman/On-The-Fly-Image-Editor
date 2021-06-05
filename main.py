import requests
from flask import Flask, make_response
from wand.image import Image
import os

app = Flask(__name__)

def resize(content,format,width,height):
    #read binary image
    with Image(blob=content) as img:
        #resize the image
        img.resize(width,height)
        #convert wand Image format to binary image
        img_binary = img.make_blob(format)
        return img_binary

def rotate(content,format,degree):
    with Image(blob=content) as img:
        img.rotate(degree)
        img_binary = img.make_blob(format)
        return img_binary

def crop(content,format,left,top,right,bottom):
    with Image(blob=content) as img:
        img.crop(left,top,right,bottom)
        img_binary = img.make_blob(format)
        return img_binary
def grayscale(content,format):
    with Image(blob=content) as img:
        img.type="grayscale"
        img_binary = img.make_blob(format)
        return img_binary

@app.route('/v1/<operation>:<parameters>/url:<path:url>')
def v1(operation,parameters, url):
    #learn format of the image to use while operating image
    format = os.path.split(url)[1].split(".")[1]
    #add http protocal to url
    url = "http://" + url
    # request the image from source website
    res = requests.request("GET", url)

    #call the method related with operation
    if operation == "resize":
        param = parameters.split("x")
        image_binary = resize(res.content,format,int(param[0]),int(param[1]))
    elif operation == "rotate":
        degree = int(parameters)
        image_binary = rotate(res.content,format,degree)
    elif operation == "crop":
        param = parameters.split("x")
        image_binary = crop(res.content, format, int(param[0]), int(param[1]),int(param[2]), int(param[3]))
    elif operation == "grayscale":
        image_binary = grayscale(res.content, format)

    #convert image to flask response
    response = make_response(image_binary)
    #define the content type by using extension of given url(format)
    contentType = "image/" + format
    #add content type to header
    response.headers.set('Content-Type', contentType)

    return response

#run the app on localhost port 8080
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)