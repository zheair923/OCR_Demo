#!/usr/bin/env python
#coding=utf-8
import sys
import os
import time
import pyttsx
import cv2
import numpy as np
from matplotlib import pyplot as plt
from aip import AipOcr
from aip import AipSpeech

reload(sys)
sys.setdefaultencoding('utf-8')

APP_ID = '' #Fill
API_KEY = '' #Fill
SECRET_KEY = '' #Fill
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def text2audio(word):
    filename="audio.mp3"
    result  = aipSpeech.synthesis(word, 'zh', 1, {'vol': 5,})
    if not isinstance(result, dict):
        with open(filename, 'wb') as f:
            f.write(result)
    else :
        print(result['error_msg'])

def image2text(filename):
    ocr_word=""
    options = {
        'detect_direction': 'true',
        'language_type': 'CHN_ENG',
        'probability' : 'false' ,
    }
    result = aipOcr.basicGeneral(get_file_content(filename), options)
    # Call api(Remote image) : result = apiOcr.basicGeneral('http://www.xxxxxx.com/img.jpg')
    for j in result['words_result']:
        ocr_word+=(j['words'])
    print(ocr_word)
    return ocr_word

def image_process(filename):
    output_filename='process.jpg'
    img = cv2.imread(filename)
    ref1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ref2 = cv2.threshold(ref1, 100, 255, cv2.THRESH_BINARY_INV)[1]
    ref3 = cv2.dilate(ref2, (2, 2), iterations=1)
    titles = ['Original Image', 'BGR2GRAY', 'threshold', 'dilate']
    images = [img, ref1, ref2, ref3]
    # for i in xrange(4):
    #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]),plt.yticks([])
    # plt.show()
    # cv2.imwrite(output_filename,ref3)
    return output_filename

if __name__ == '__main__':
    out=image_process('testimg.jpg')
    word=image2text(out)
    text2audio(word)
    # engine = pyttsx.init()
    # engine.say(word)
    # engine.runAndWait()
