import os
import csv
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reviewduk.settings")
from django.conf import settings

parseStr = lambda x: float(x) if '.' in x else int(x)

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
            sample.append(row[2][2:-2])
    return sample

def readPredictFile():
    y_pred = []
    with open(settings.PREDICT, 'rb') as csvfile:
        predictions = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in predictions:
            pred = parseStr(row[0])
            y_pred.append(pred)
    return y_pred
