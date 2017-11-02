from django.shortcuts import *
from django.template import RequestContext
from django.contrib.auth import *
from django.contrib.auth.models import Group, User
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import Max,Count
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from monitoreo.models import *
from django.db import transaction
from django.contrib.auth.hashers import *
from django.core.mail import send_mail
from django.db import connection
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth import authenticate

import xlrd
import json 
import csv
import simplejson
import xlwt
import requests
import os
import collections

def dash(request):

	return render(request,'monitoreo/index.html')


def data(request):

	return render(request,'monitoreo/data.html')


def llamadas(request):

	data=MLlamadas.objects.all().values('estado__descripcion').order_by('id').annotate(num_est=Count('estado'))

	print data

	data_dict = ValuesQuerySetToDict(data)

	data = simplejson.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")

def tipollamadas(request):

	data=MLlamadas.objects.all().values('estado__descripcion','tipo').order_by('id').annotate(num_est=Count('tipo'))

	print data

	data_dict = ValuesQuerySetToDict(data)

	data = simplejson.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")

def anexos(request):

	data=MAnexos.objects.all().values('n_anexo','estado__id','estado__descripcion','ip_anexo','ip_servidor','origen','destino')

	print data

	data_dict = ValuesQuerySetToDict(data)

	data = simplejson.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")

def errores(request):

	data=MErrores.objects.all().values('descripcion').annotate(num_est=Count('id'))

	print data

	data_dict = ValuesQuerySetToDict(data)

	data = simplejson.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


def ValuesQuerySetToDict(vqs):
   
   return [item for item in vqs]

@csrf_exempt
def filtermadafaca(request):

	if request.method=='POST':

		print request.GET

	return HttpResponse('OK', content_type="application/json")