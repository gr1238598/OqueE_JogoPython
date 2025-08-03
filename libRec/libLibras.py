import cv2
import numpy as np
import pygame
from tensorflow.keras.models import load_model
from PIL import Image
from tensorflow.keras.preprocessing import image

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.constraints import max_norm

def nothing(x):
    pass

image_x, image_y = 64, 64


# classifier = load_model('../models/cnn_model_LIBRAS_20190531_0135.h5')
classifier = load_model('libRec/cnn_model_LIBRAS_20190606_0106.h5')

classes = 21
letras = {'0' : 'a', '1' : 'b', '2' : 'c' , '3': 'd', '4': 'e', '5':'f', '6':'g', '7': 'i', '8':'l', '9':'m', '10':'n', '11': 'o', '12':'p', '13':'q', '14':'r', '15':'s', '16':'t', '17':'u', '18':'v', '19':'w','20':'y'}

def cvimage_to_pygame(image):
    return pygame.image.frombuffer(image.tobytes(), image.shape[:2],"RGB")

def most_frequent(List):
    return max(set(List), key = List.count)

def predictor():
       test_image = image.load_img('libRec/temp/img.png', target_size=(64, 64))
       test_image = image.img_to_array(test_image)
       test_image = np.expand_dims(test_image, axis = 0)
       result = classifier.predict(test_image)


       maior, class_index = -1, -1

       for x in range(classes):

           if result[0][x] > maior:
              maior = result[0][x]
              class_index = x

       return [result, letras[str(class_index)]]

async def reconhece():

    cam = cv2.VideoCapture(0)

    img_counter = 0

    img_text = ['','']
    listPerd=[]
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame,1)


        img = cv2.rectangle(frame, (425,100),(625,300), (0,255,0), thickness=2, lineType=8, shift=0)

        imcrop = img[102:298, 427:623]

        #cv2.putText(frame, str(img_text[1]), (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        #cv2.imshow("test", frame)
        #cv2.imshow("mask", imcrop)

        img_name = "libRec/temp/img.png"
        save_img = cv2.resize(imcrop, (image_x, image_y))
        cv2.imwrite(img_name, save_img)
        img_text = predictor()

        if len(listPerd) < 4:
            listPerd.append(str(img_text[1]))
        else:
            #print(most_frequent(listPerd))
            return [most_frequent(listPerd),cvimage_to_pygame(imcrop)]


    cam.release()
    cv2.destroyAllWindows()
