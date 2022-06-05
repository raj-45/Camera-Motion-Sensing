# import the opencv module
import cv2
import keyboard
import pygame
import requests

bot_token = '5252564895:AAF5qfWspdy9zFKNpOdMUTzXIKOKNRRkDz8'
chat_id = "-639058363"
text = "Intruder alert"
file = r"NewPicture.jpg"
files = {
    'photo': open(file, 'rb')
}

# capturing video
capture = cv2.VideoCapture(0)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("alarm.mp3")

while capture.isOpened():
    # to read frame by frame
    _, img_1 = capture.read()
    _, img_2 = capture.read()

    # find difference between two frames
    diff = cv2.absdiff(img_1, img_2)

    # to convert the frame to grayscale
    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    # apply some blur to smoothen the frame
    diff_blur = cv2.GaussianBlur(diff_gray, (5, 5), 0)

    # to get the binary image
    _, thresh_bin = cv2.threshold(diff_blur, 20, 255, cv2.THRESH_BINARY)

    # to find contours
    contours, hierarchy = cv2.findContours(
        thresh_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # to draw the bounding box when the motion is detected
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if cv2.contourArea(contour) > 300:
            cv2.rectangle(img_1, (x, y), (x+w, y+h), (0, 255, 0), 2)
            pygame.mixer.music.play()
            result = 5
            while(result > 0):
                ret, frame = capture.read()
                cv2.imwrite("NewPicture.jpg", frame)
                result = result - 1
            base_url = 'https://api.telegram.org/bot5252564895:AAF5qfWspdy9zFKNpOdMUTzXIKOKNRRkDz8/sendMessage?chat_id=-639058363&text="{}"'.format(text)
            requests.get(base_url)
            resp = requests.post('https://api.telegram.org/bot5252564895:AAF5qfWspdy9zFKNpOdMUTzXIKOKNRRkDz8/sendPhoto?chat_id=-639058363',files=files)

    cv2.imshow("Detecting Motion...", img_1)
    if keyboard.is_pressed('q'):  # if key 'q' is pressed
        exit()
    if keyboard.is_pressed('s'):  # if key 'q' is pressed
        pygame.mixer.music.stop()
    if cv2.waitKey(100) == 13:
        exit()
