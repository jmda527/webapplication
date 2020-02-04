from django.shortcuts import render,redirect
from seperate.model_create import Trash_sep
from google.cloud import storage
from urllib.parse import urlencode,parse_qs
import pickle
import glob
import os


def load_model(place):
    bucket_name = 'jmda-seperate-265706.appspot.com'
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob('files/{}.pkl'.format(place))
    seperator = pickle.loads(blob.download_as_string())
    return seperator

place_list = ['危險物品管理組','民力運用組','災害管理組','綜合企劃組']
seperator_list = {i:load_model(i) for i in place_list}


# Create your views here.
def select(request):
    return render(request, 'seperate/select.html')

def nextpage(request):
    place = request.POST['place']
    place = urlencode({'place':'危險物品管理組'})

    response = redirect('/seperate/query')
    response.set_cookie('place',place,max_age=7*24*3600)
    return response

def query(request):
    if 'place' in request.COOKIES:
        return render(request, 'seperate/query.html')
    else:
        return render(request, 'seperate/select.html')

def sep_check(request):
    text = request.GET['content']
    place = request.COOKIES['place']
    place = parse_qs(place)['place'][0]
    name_list,score_list,first_score = seperator_list[place].predicting(text)
    return render(request, 'seperate/sep_check.html',
                  {'content':text,'name':name_list,'score':score_list,'first_score':first_score})

def upload(request):
    return render(request,'seperate/upload.html')

def proccess(request):
    place = request.POST['place']
    data = request.FILES['xlsx']
    seperator = Trash_sep(place)
    seperator.preproccessing_direct(data)
    seperator_list[place] = seperator
    file = pickle.dumps(seperator)

    #save in google cloud storage
    bucket_name = 'jmda-seperate-265706.appspot.com'
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.get_blob('files/{}.pkl'.format(place))
    blob.upload_from_string(file)
    return render(request,'seperate/proccess.html',{'place':place})
