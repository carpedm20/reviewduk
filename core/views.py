#-*- coding: utf-8 -*-
import os
import random
import subprocess
import simplejson

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from utils.func import *

predictCommand = ("vw -t -d %s -i %s -p %s" % (settings.SAMPLE,
                                               settings.MODEL,
                                               settings.PREDICT)).split(' ')
environmentDict=dict(os.environ, LD_LIBRARY_PATH='/usr/local/lib')    

def index(request):
    template = 'index.html'

    return render(request, template)

@csrf_exempt
def get_prediction(request):
    global environmentDict, predictCommand
    template = 'index.html'

    if not request.POST:
        return render(request, template)
    else:
        response_dict = {}

        text = request.POST.get("text","")

        with open(settings.TEST, 'w') as predict:
            predict.write('1 1 |f %s |a %s' % (text, len(text)))

        command = ("vw -t -d %s -i %s -p %s" % (settings.TEST,
                                                settings.MODEL,
                                                'out.vw')).split(' ')
        subprocess.call(command, env=environmentDict)

        samples = readSampleFile(settings.TEST)
        predictions = readPredictFile('out.vw')

        response_dict['data'] = [{'text':text, 'pred':pred} for text,pred in zip(samples, predictions)]

        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')

def get_cached_prediction(request, count):
    if count > 30:
        count = 30

    #with open(settings.TOTAL_SAMPLE) as totalf:
    with open(settings.SAMPLE) as totalf:
        lines = totalf.readlines()
        random.shuffle(lines)
        lines = lines[:count]

        response_dict = {}

        # original, pred, code, text
        response_dict['data'] = [{'poster': poster_url(line.split()[2]),
                                  'code':line.split()[2],
                                  'original':line.split()[0],
                                  'pred':line.split()[1],
                                  'text':' '.join(line.split()[3:])} for line in lines]
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')

def get_review(request, count = 30):
    global environmentDict, predictCommand
    if count > 30:
        count = 30

    response_dict = {}

    get_sample(count)
    subprocess.call(predictCommand, env=environmentDict)

    samples = readSampleFile()
    predictions = readPredictFile()

    response_dict['data'] = [{'poster': poster_url(rev[0]),
                              'code':rev[0],
                              'text':rev[1],
                              'pred':pred} for rev,pred in zip(samples, predictions)]

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')
