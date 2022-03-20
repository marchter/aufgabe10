from picamera import PiCamera
from time import sleep
from uuid import uuid4

camera = PiCamera()

camera.start_preview()
sleep(5)
unique_id = str(uuid4())
camera.capture("/home/pi/aufgabe10/static/"+unique_id+".jpg")
camera.stop_preview()
