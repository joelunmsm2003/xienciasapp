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
from django.db import transaction
from django.contrib.auth.hashers import *
from django.core.mail import send_mail
from django.db import connection
from django.utils.six.moves import range
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt

import xlrd
import json 
import csv
import simplejson
import xlwt
import requests
import os
import datetime
import collections

from datetime import datetime
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict


def buscar(request):

	if request.method == 'POST':

		print request.POST

		valor = request.POST['valor']
		inicio = request.POST['inicio']
		fin = request.POST['fin']
		elemento = request.POST['elemento']
		inicio = str(inicio)
		fin = str(fin)
		con=0

		if inicio != '':

			inicio = datetime.strptime(inicio, "%d %B, %Y")

		else:

			inicio ='2000-01-01 00:00:00'

		if fin != '':

			fin = datetime.strptime(fin, "%d %B, %Y")

		else:

			fin = '4000-01-01 00:00:00'

		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		if elemento != 'none' and valor != '':

			print inicio,'-',fin

			print 'sql',"SELECT id,src,dst,calldate,disposition,duration,billsec FROM cdr where   calldate >='" + str(inicio) + "' and calldate <= '" + str(fin) + "' and " + elemento + " = '"+ valor +"' ORDER BY id DESC"

			for row in Cdr.objects.raw("SELECT id,src,dst,calldate,disposition,duration,billsec FROM cdr where (calldate >='" + str(inicio) + "' and calldate <= '" + str(fin) + "' and " + elemento + " = '"+ valor +"' ORDER BY id DESC"):

				d = collections.OrderedDict()
				d['id'] = row.id
				d['src'] = row.src
				d['dst'] = row.dst
				d['disposition'] = row.disposition
				d['duration'] = row.duration
				d['billsec'] = row.billsec
				d['calldate'] = row.calldate.strftime(fmt)
				con=con+1
			
				objects_list.append(d)

				

		if elemento == 'none' and valor == '':

			print inicio,'-',fin

			for row in Cdr.objects.raw("SELECT id,src,dst,calldate,disposition,duration,billsec FROM cdr where (dst=7028425 or LENGTH(src) = 3 or LENGTH(dst)= 3) and calldate >='" + str(inicio) + "' and calldate <= '" + str(fin) + "' ORDER BY id DESC"):

				d = collections.OrderedDict()
				d['id'] = row.id
				d['src'] = row.src
				d['dst'] = row.dst
				d['disposition'] = row.disposition
				d['duration'] = row.duration
				d['billsec'] = row.billsec
				d['calldate'] = row.calldate.strftime(fmt)
				con=con+1
			
				objects_list.append(d)

			


	
		 
		return render(request, 'cdr/filtro.html',{'data':objects_list,'con':con})


			



def campania(request):

    x=Cdr._meta.get_all_field_names()
    data_json = simplejson.dumps(x)
    i=i
    for x in x:

    	Table(id=i,idoname=x,status=0).save()
    	i=i+1

    return HttpResponse(data_json, content_type="application/json")


def field(request):

    x=Cdr._meta.get_all_field_names()
    data_json = simplejson.dumps(x)
    i=i
    for x in x:

    	Table(id=i,idoname=x,status=0).save()
    	i=i+1

    return HttpResponse(data_json, content_type="application/json")

def cant(request):


	objects_list = []
	answer = 0
	noanswer = 0

	for row in Cdr.objects.raw('SELECT id, dst,src,disposition FROM cdr   ORDER BY id DESC'):


		d = collections.OrderedDict()


		if row.disposition == 'ANSWERED':
			answer =answer+1
			

		if row.disposition == 'NO ANSWER':
			noanswer = noanswer +1
			
		
		d['answer'] = answer
		d['noanswer'] = noanswer


	objects_list.append(d)

	j = json.dumps(objects_list)


	return HttpResponse(j, content_type="application/json")


def lol(request):


	data=Cdr.objects.filter(calldate__month=6)


	data_dict = ValuesQuerySetToDict(data)

	data_json = simplejson.dumps(data_dict)

	print data

	return HttpResponse(data_json, content_type="application/json")


def date_handler(obj):

    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

def graph(request):

	return render(request,'o.html')

def home(request):

	return render(request,'cdr/home.html')





def report(request):



		objects_list = []
		fmt = '%Y-%m-%d %H:%M:%S %Z'


		for row in Cdr.objects.raw('SELECT id,src,dst,calldate,disposition,duration,billsec FROM cdr  ORDER BY id DESC'):

			d = collections.OrderedDict()
			d['id'] = row.id
			d['src'] = row.src
			d['dst'] = row.dst
			d['disposition'] = row.disposition
			d['duration'] = row.duration
			d['billsec'] = row.billsec
			d['calldate'] = row.calldate.strftime(fmt)
		
			objects_list.append(d)

		j= json.dumps(objects_list)

	
		 
		return HttpResponse(j, content_type="application/json")



def ingresar(request):

	if request.user.is_authenticated():

		return HttpResponseRedirect("/report")

	else:

		if request.method == 'POST':

			print request.POST

			user = request.POST['user']
			
			psw = request.POST['password']

			user = authenticate(username=user, password=psw)

		
			if user is not None:

				if user.is_active:

					login(request, user)

					return HttpResponseRedirect("/report")

			else:
				return HttpResponseRedirect("/ingresar")
		
		else:

			return render(request, 'cdr/logear.html',{})

def salir(request):

	logout(request)
	
	return HttpResponseRedirect("/ingresar")