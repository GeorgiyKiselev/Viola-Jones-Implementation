# %%
import cv2
import numpy as np
import sys
import time
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# %%
def update_scale_factor(value):
    global scale_factor
    scale_factor = value/100

def update_min_neighbors(value):
    global min_neighbors
    min_neighbors = value

scale_factor = 1.05
min_neighbors = 1

def upload_file():
    root = tk.Tk()

    file_path = filedialog.askopenfilename(
        title="Select an Image or Video",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
                   ("Video Files", "*.mp4;*.avi;*.mov;*.mkv")]
    )

    if file_path:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file = Image.open(file_path)
            print("Image successfully loaded!")
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            file = cv2.VideoCapture(file_path)
            print("Video successfully loaded!")
        else:
            print("Unsupported file format.")
            return None

        return file_path
    else:
        print("No file selected.")
        return None, None

def detect_img():
    try:
        user_input = int(input("Image Upload: Enter '1' to use camera. Enter '2' to upload from device. Enter 'Ctrl + C' to cancel."))
        if user_input not in [1, 2]:
            raise ValueError("Invalid input, select '1' or '2'.")

    except ValueError as e:
        print(e)
        return detect_img()
    
    except KeyboardInterrupt:
        print("\nUser exited the program.")
        sys.exit(0)

    if user_input == 1:
        print("Utilizing primary webcam...")
        cap = cv2.VideoCapture(0)
        if cap is None or not cap.isOpened():
            print("Primary webcam not found. Accessing phone webcam. Please install 'IP Webcam' on mobile device.")
            cap = cv2.VideoCapture('https://192.168.239.109:8080/video')
            if cap is None or not cap.isOpened():
                print("No webcams found. Try again.")
                return detect_img()
            
    else:
        cap = upload_file()
        

    return cap

# %%
front_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
side_cascade = cv2.CascadeClassifier("data/haarcascade_profileface.xml")

cap = detect_img()
window_name = "Image"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1200, 900)
cv2.createTrackbar("Scale Factor", "Image", 105, 200, update_scale_factor)
cv2.createTrackbar("Min Neighbors", "Image", 1, 20, update_min_neighbors)


if type(cap) == cv2.VideoCapture:
    
    while True:
        ret, img = cap.read()

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = front_cascade.detectMultiScale(gray, 1.05, 4, minSize=(30, 30))
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            side = side_cascade.detectMultiScale(roi_gray, 1.05, 4, minSize=(30, 30))
            for (ex,ey,ew,eh) in side:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

        cv2.imshow('Image', img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


else:
    while True:
        img = cv2.imread(cap)


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = front_cascade.detectMultiScale(gray, scale_factor, min_neighbors, minSize=(30, 30))
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            side = side_cascade.detectMultiScale(roi_gray, scale_factor, min_neighbors, minSize=(30, 30))
            for (ex,ey,ew,eh) in side:
                cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0,255,0), 2)

        cv2.imshow("Image", img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cv2.destroyAllWindows()



