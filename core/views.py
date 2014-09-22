import os
import subprocess
import simplejson

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from utils.func import *

predictCommand = ("vw -t -d %s -i %s -p %s" % (settings.SAMPLE,
                                               settings.MODEL,
                                               settings.PREDICT)).split(' ')
environmentDict=dict(os.environ, LD_LIBRARY_PATH='/usr/local/lib')    

def index(request):
    template = 'index.html'

    return render(request, template)

def get_prediction(request):
    global environmentDict, predictCommand
    template = 'index.html'

    if not request.POST:
        return render(request, template)
    else:
        response_dict = {}

        with open(settings.PREDICT, 'w') as predict:
            predict.write('1 1 |f %s |a %s' % (text, len(text)))

        subprocess.call(predictCommand, env=environmentDict)

        samples = readSampleFile()
        predictions = readPredictFile()

        response_dict['data'] = [{'text':text, 'pred':pred} for text,pred in zip(samples, predictions)]

        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')

def get_review(request, count):
    global environmentDict, predictCommand

    response_dict = {}

    get_sample(20)
    subprocess.call(predictCommand, env=environmentDict)

    samples = readSampleFile()
    predictions = readPredictFile()

    response_dict['data'] = [{'poster': poster_url(rev[0]),
                              'code':rev[0],
                              'text':rev[1],
                              'pred':pred} for rev,pred in zip(samples, predictions)]

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')
