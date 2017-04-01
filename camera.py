from picamera import PiCamera
from time import sleep
import requests
import json
import serial

headers = {
        'Content-Type': 'application/octet-stream',
        'Host': 'westus.api.cognitive.microsoft.com',
        'Ocp-Apim-Subscription-Key': ''
    }

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SIXTEENBITS,
    timeout=1
    )

camera = PiCamera()

camera.start_preview()
camera.preview.alpha = 128
camera.resolution = ( 2592 , 1944 )
for i in range(10):
    sleep(2)
    path = '/home/pi/Desktop/image' + str(i) + 's.jpg'
    camera.capture(path)
    r = requests.post(url="https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=false", headers=headers, data= open(path, "br"))
    resp = json.loads(r.text)
    print('Len resp : ' + str(len(resp)))
    if resp:
        print('Top : ' + str(resp[0]['faceRectangle']['top']))
        print('Height : ' + str(resp[0]['faceRectangle']['height']))
        print('Width : ' + str(resp[0]['faceRectangle']['width']))
        print('Left : ' + str(resp[0]['faceRectangle']['left']))
        coords = {'X':,}
        ser.write()
camera.stop_preview()

# key 1:548f653e1dbd46b8a687e581b8884ee0

