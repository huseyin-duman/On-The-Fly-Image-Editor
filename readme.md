
# On The Fly Image Editor

On The Fly Image Editor is a web server which can resize, crop, rotate and grayscale an image from a given url. It is developed in python by using Flask and ImageMagick. 

You need to open your browser and type your request after running the server, in the format which is given below.
http://[hostname]:[port]/v1/[operation]:[parameters]/url:[image url without the protocol] 
In given code [hostname] is localhost or 127.0.0.1 and [port] is 8080.
[operation] can be resize, rotate,crop,or grayscale.
[parameters] are depends according to your operation. 
For resize you need to write [width]x[height]. For example 640x360.
For rotate you need to write [degree]. For example 90.
For crop you need to write [left]x[top]x[right]x[bottom]. For example 10x20x150x300.
For grayscale you can write anything but it must not bu empty. Best is the putting -.
[image url without the protocol]  can be an image from a website. For example, upload.wikimedia.org/wikipedia/commons/b/b1/VAN_CAT.png or upload.wikimedia.org/wikipedia/commons/5/5d/Akbash_Dog_male_2016.jpg
This is the full url example which you can type your browser. 
http://localhost:8080/v1/resize:640x360/url:upload.wikimedia.org/wikipedia/commons/b/b1/VAN_CAT.png


## Environment Setup and Initialization:

To setup environment install required packages to virtual environment. Navigate to the project folder on cmd and create an virtual environment and install requirements. Requirements include flask, requests and wand. 
```bash
py -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```
Also to use wand you need to install ImageMagick on your pc. You can downlad and install ImageMagick from https://imagemagick.org/script/download.php#windows

To start server.

```bash
python main.py
```

Now you can open your browser and type the url in the format given at the begining.

## Close Look to Code:
There is 1 .py folder in the project, main.py. 

First import relevant libraries.
```python
import requests  
from flask import Flask, make_response  
from wand.image import Image  
import os
```
There is only one page creater in the code. It gets the operation, parameters and img url from the browser. Firstly requests image from given url. After that performs operation on it accordign to given parameters and represents output image to user. In that process code does not save the image anywhere all the process is on the fly.
```python
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
```
There are also other methods to handle operations (resize,rotate,crop and grayscale) by ImageMagick. 
```python
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
```
Finally main.py run the app on local server.
```python
#run the app on localhost port 8080  
if __name__ == "__main__":  
    app.run(host="127.0.0.1", port=8080, debug=True)
```
