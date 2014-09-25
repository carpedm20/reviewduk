#-*- coding: utf-8 -*-
import re
import os, sys
import csv
import random
import requests
import codecs
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewduk.settings")
from django.conf import settings

parseStr = lambda x: float(x) if '.' in x else int(x)

def clean(s):
    try:
        s = s.encode('utf-8')
    except:
        pass
    try:
        return " ".join(re.findall(r'[가-힣\w]+', s, flags=re.UNICODE|re.LOCALE)).decode('utf-8').lower()
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return False
    #return " ".join(s.split())

def poster_url(code):
    b = BeautifulSoup(requests.get('http://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+code).text)
    try:
        img = b.find('img')
        return [img['src']+"?type=m203_290_2", img['alt']]
    except:
        return ['http://static.naver.net/movie/2012/06/dft_img203x290.png','']

def get_sample(count = 10):
    train_name = settings.TRAIN
    out_name = settings.SAMPLE

    with open(train_name) as trainf, open(out_name, 'w') as outf:
        lines = trainf.readlines()
        random.shuffle(lines)

        outf.writelines(lines[:count])

def readSampleFile(file_name = settings.SAMPLE):
    sample = []
    with open(file_name, 'rb') as csvfile:
        predictions = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in predictions:
            sample.append((row[1][1:], row[2][2:-2]))
    return sample

def readPredictFile(file_name = settings.PREDICT):
    y_pred = []

    with open(file_name, 'rb') as csvfile:
        predictions = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in predictions:
            pred = parseStr(row[0])
            y_pred.append(pred)
    return y_pred
