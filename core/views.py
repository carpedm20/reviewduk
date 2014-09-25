#-*- coding: utf-8 -*-
import os
import random
import subprocess
import simplejson
import codecs

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

    if request.method == 'POST':
        response_dict = {}

        text = request.POST.get("text","").encode('utf-8')

        if text == "":
            l=open('vw_models/sample_wxtchx_train.vw').readlines()
            random.shuffle(l)
            vw_text = l[0]
            #reviews = ['이 영화의 두마디 나의 선장님 현재를 즐겨라 이것만으로도 별점10개는 충분하다', '배우의 연기는 좋았다', '시간 아까웠다', '믿고 보는 디카프리오', '동심으로 돌아갈 수 있었다', '미야자키 하야오의 표현력은 역시 대단했다', '그저 그런 영화중 하나', '돈주고 보기는 아까운 영화','이거 골든라즈베리 수상작이었네','포스터만 봐도 싸구려 저질 냄세가 폴폴난다','잘 만든 영화 영화가 끝난 후 엔딩크레딧보면 기분이 묘해짐 왜일까','재미없어요ㅡㅡ 정우성이라는 큰 그릇을 왜 이렇게만들었는지 준호가 제일 연기잘햇네요','볼만했다 마지막장면 억지로 끼워놨다고 누가 말해서 답답함에 쓴다 영화 잘보면 걔가 어떤식으로 이어져있는지 알수있다 더이상말하면 스포지만 영화 제대로 안보고 억지니 뭐니 하지는 말자','배우들 다연기잘했는데 뭔가부족한느낌 근데 연기는 진짜잘하네요','개인적인 취향이 있겠지만 재밋고 집중력있게 볼 수 있는영화라고 생각합니다']
            #random.shuffle(reviews)
            #text = reviews[0]
        else:
            vw_text = '1 1 |f %s |a %s' % (text.replace(',',''), len(text))

        with open(settings.TEST, 'w') as predict:
            predict.write(vw_text)

        command = ("vw -t -d %s -i %s -p %s" % (settings.TEST,
                                                'vw_models/w_model.vw',
                                                'out.vw')).split(' ')
        subprocess.call(command, env=environmentDict, stdout=subprocess.PIPE)

        samples = readSampleFile(settings.TEST)
        predictions = readPredictFile('out.vw')

        response_dict['data'] = [{'text':text, 'pred':int(pred)} for text,pred in zip(samples, predictions)]

        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')
    else:
        return render(request, template)

def get_cached_prediction(request, count):
    if count > 50:
        count = 50

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
    subprocess.call(predictCommand, env=environmentDict, stdout=subprocess.PIPE)

    samples = readSampleFile()
    predictions = readPredictFile()

    response_dict['data'] = [{'poster': poster_url(rev[0]),
                              'code':rev[0],
                              'text':rev[1],
                              'pred':pred} for rev,pred in zip(samples, predictions)]

    return HttpResponse(simplejson.dumps(response_dict), mimetype='application/; charset=utf-8')
