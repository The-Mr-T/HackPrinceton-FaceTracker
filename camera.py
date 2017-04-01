from picamera import PiCamera
from time import sleep
import requests
import json

headers = {
        'Content-Type': 'application/octet-stream',
        'Host': 'westus.api.cognitive.microsoft.com',
        'Ocp-Apim-Subscription-Key': ''
    }

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
        top = resp[0]['faceRectangle']['top']
        height = resp[0]['faceRectangle']['height']
        width =resp[0]['faceRectangle']['width']
        left = resp[0]['faceRectangle']['left']

        centerX = left + (width / 2)
        centerY = top + (height / 2)

        diff_x = centerX - 1296
        diff_y = centerY - 972

        # Greater enough difference in X
        if(float(diff_x) > 2592 * 0.05):
            print("diff_x : " + str(diff_x) )
            # Here we determine how much we need to correct
        # Greater enough difference in Y
        if(float(diff_y) > 1944 * 0.05):
            print("diff_y : " + str(diff_y))
camera.stop_preview()

# key 1:548f653e1dbd46b8a687e581b8884ee0


