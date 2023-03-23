from picamera2 import Picamera2, Preview
import time
import requests
import base64 
from gpiozero import LED
from signal import pause
from gpiozero import Button
import random

green_led = LED(4)
red_led = LED(17)
button = Button(16)

positive = ['HAPPY', 'SURPRISED', 'CALM']
negative = ['ANGRY', 'CONFUSED', 'SCARED', 'SAD']

emotions = ['HAPPY', 'SURPRISED', 'CALM', 'ANGRY', 'CONFUSED', 'SCARED', 'SAD']
points = [0]

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
picam2.configure(camera_config)
picam2.start()

random_emotions = [random.choice(emotions)]

def takePicture():
    time.sleep(1)
    picam2.capture_file("test.jpg")
    time.sleep(1)

def seeEmotion():
    if green_led.is_active or red_led.is_active:
        green_led.off()
        red_led.off()
        return
    print("----------------------------------")
    print("Taking a picture..")
    takePicture()

    print("Took picture, sending it to the api")
    print("----------------------------------")
    print("")

    with open("test.jpg", "rb") as image_file: 
        encoded_string = base64.b64encode(image_file.read()).decode("utf8")


    
    # api_call = requests.post("https://api.server.cameralyze.co/flow/1a7ad4bd-7824-4224-86b0-cae222e8889e", json={"apiKey": "PnlVAL9X9dkvQ9ur", "image": encoded_string})
    # api_call = requests.post("https://api.server.cameralyze.co/endpoint/1a7ad4bd-7824-4224-86b0-cae222e8889e", json={"apiKey": "PnlVAL9X9dkvQ9ur", "image": encoded_string})
    # print(api_call)
    # response = api_call.json() 

    # print("Got the api response: ")
    # print(response)
    # emotion = response['data']['detections'][0]['name']

    api_call = requests.post("https://api.server.cameralyze.co/model/b66919e1-d92d-4e82-80d7-1b36ccaa29fb", json={"apiKey": "PnlVAL9X9dkvQ9ur", "image": encoded_string})
    response = api_call.json() 


    try:
        emotion = response['data']['data'][0][5]
        print("----------------------------------")
        print("The emotion detected was:")
        print(emotion)

        if emotion == random_emotions[0]:
            print("You showed the correct emotion!") 
            points[0] = points[0] + 1
            green_led.on()
        else:
            print("You showed the incorrect emotion!") 
            red_led.on()

        
        # if emotion in positive:
        #     green_led.on()
        # elif emotion in negative:
        #     red_led.on()
        # else:
        #     green_led.on()
        #     red_led.on()
    except Exception as e:
        print("There was a problem finding your face.")
        red_led.on()
    
    
    
    print("----------------------------------")
    print("")

    random_emotions[0] = random.choice(emotions)

    print("----------------------------------")

    print("Try to show the following emotion: ")
    print(random_emotions[0])


    print("Points earned so far: ")
    print(points[0])
    print("----------------------------------")
    print("")



print("----------------------------------")
print("Try to show the following emotion: ")
print(random_emotions[0])


print("Points earned so far: ")
print(points[0])
print("----------------------------------")
print("")

button.when_pressed = seeEmotion

pause()




#
# Text recognition

# def ocr_space_file(filename, overlay=False, api_key='K89916831388957', language='eng'):
#     """ OCR.space API request with local file.
#         Python3.5 - not tested on 2.7
#     :param filename: Your file path & name.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     with open(filename, 'rb') as f:
#         r = requests.post('https://api.ocr.space/parse/image',
#                           files={filename: f},
#                           data=payload,
#                           )
#     return r.json()
#     # return r.content.decode()


# def ocr_space_url(url, overlay=False, api_key='K89916831388957', language='eng'):
#     """ OCR.space API request with remote file.
#         Python3.5 - not tested on 2.7
#     :param url: Image url.
#     :param overlay: Is OCR.space overlay required in your response.
#                     Defaults to False.
#     :param api_key: OCR.space API key.
#                     Defaults to 'helloworld'.
#     :param language: Language code to be used in OCR.
#                     List of available language codes can be found on https://ocr.space/OCRAPI
#                     Defaults to 'en'.
#     :return: Result in JSON format.
#     """

#     payload = {'url': url,
#                'isOverlayRequired': overlay,
#                'apikey': api_key,
#                'language': language,
#                }
#     r = requests.post('https://api.ocr.space/parse/image',
#                       data=payload,
#                       )
#     return r.json()
#     # return r.content.decode()


# # Use examples:
# test_file = ocr_space_file(filename='test.jpg', language='pol')


# print("-----------")
# print("The texts we parsed were: ")
# for result in test_file["ParsedResults"]:
#     print(result["ParsedText"])
# print("-----------")




# test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')



#
# Another text recognition

# api_key = "MzaIUOVNYK3YyM2OcxKj6w==kCI7ydHzWFbonMCP"
# api_url = 'https://api.api-ninjas.com/v1/imagetotext'
# image_file_descriptor = open('test.jpg', 'rb')
# files = {'image': image_file_descriptor}
# headers = {'X-Api-Key': api_key}
# r = requests.post(api_url, files=files, headers=headers)
# print(r.json())
