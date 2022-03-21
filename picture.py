from picamera import PiCamera
from dataclasses import dataclass
from time import sleep
from uuid import uuid4
from io import BytesIO
import base64
import base64
import requests

# was aufm pi passiert:
# war nur a idee und wollte mal was mit uuid probieren

#camera = PiCamera()
#
#camera.start_preview()
#sleep(5)
#unique_id = str(uuid4())
#camera.capture("/home/pi/aufgabe10/static/" + unique_id + ".jpg")
#camera.stop_preview()


#Leider 14 minuten zu spät :D


def get_base64_encoded_image(image):
    with open(image, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def decode_image(image, data):
    with open(image, 'wb') as img_file:
        decoded_data = base64.decodebytes(data.encode('utf-8'))
        img_file.write(decoded_data)

#TODO: Calls
my_stream = BytesIO()
camera = PiCamera()
sleep(5)
camera.capture(my_stream, 'jpeg')
base64 = base64.b64encode(my_stream.getvalue()).decode()
print(base64)

test = {'name': 'test', 'description': 'test image', 'who': 'test', 'data': base64 }
print(test)
response = requests.put('http://0.0.0.0/picture_meta/0' , json=test)
print(response)
res_json = response.json()
print(res_json)

response = requests.get('http://0.0.0.0/picture_meta/0').json()
print(response)
decode_image('/home/pi/aufgabe10/static/', res_json['data'])