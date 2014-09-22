import os
import csv
import random
import requests
from bs4 import BeautifulSoup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewduk.settings")
from django.conf import settings

parseStr = lambda x: float(x) if '.' in x else int(x)

def poster_url(code):
    b = BeautifulSoup(requests.get('http://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode='+code).text)
    img = b.find('img')
    return [img['src'], img['alt']] or ''

def get_sample(count = 10):
    train_name = settings.TRAIN
    out_name = settings.SAMPLE

    with open(train_name) as trainf, open(out_name, 'w') as outf:
        lines = trainf.readlines()
        random.shuffle(lines)

        outf.writelines(lines[:count])

def readSampleFile():
    sample = []
    with open(settings.SAMPLE, 'rb') as csvfile:
        predictions = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in predictions:
            sample.append((row[1][1:], row[2][2:-2]))
    return sample

def readPredictFile():
    y_pred = []
    with open(settings.PREDICT, 'rb') as csvfile:
        predictions = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in predictions:
            pred = parseStr(row[0])
            y_pred.append(pred)
    return y_pred
