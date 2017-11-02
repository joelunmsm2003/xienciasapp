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
from appxiencias.models import *
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
from datetime import datetime,timedelta

import xlrd
import json 
import csv
import simplejson
import xlwt
import requests
import os
import collections
import base64
import mad
import time



def logear(request):


	if request.user.is_authenticated():

		return HttpResponse('autentificado', content_type="application/json")

	else:

		if request.method == 'POST':

			data = json.loads(request.body)

			user = data['username']
			
			psw = data['password']

			user = authenticate(username=user, password=psw)

		
			if user is not None:

				if user.is_active:

					login(request, user)

					return HttpResponse('autentificado', content_type="application/json")


			else:

				return HttpResponse('noautentificado', content_type="application/json")
		
		else:

			return HttpResponse('noautentificado', content_type="application/json")

def date_handler(obj):

    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]

@login_required(login_url="/ingresar")

def estados(request,database,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	m = [1,2]

	d = []

	for i in m:

		c = Traficosms.objects.using(database).filter(lote_id=lote,status=i).count()
		d.insert(0,c)

	print d 
	
		
	data = json.dumps(d)
	
	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def estadosblaster(request,database,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	m = [0,1]

	d = []

	print 'lote',lote

	for i in m:

		c = DBlaster.objects.using(database).filter(lote_id=lote,lestado=i).count()
		d.insert(0,c)

	print d 
	
		
	data = json.dumps(d)
	
	return HttpResponse(data, content_type="application/json")



def cancelarlotesms(request,id):

	database='MTC'

	evento=Lote.objects.using(database).get(id=id)
	fecha = datetime.now()
	fecha= fecha-timedelta(hours=5)
	evento.fecha = fecha
	evento.aprobar=0

	evento.save(using=database)

	return HttpResponse('dato', content_type="text/json")


@login_required(login_url="/ingresar")

def proceso(request,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	dllam = DLlamadas.objects.using(database).filter(flagfin=0).values('id_d_blaster','destino','d_total')

	for i in range(len(dllam)):

		dllam[i]['lote']=DBlaster.objects.get(id_d_blaster=dllam[i]['id_d_blaster']).lote

		

	data_dict = ValuesQuerySetToDict(dllam)	

	data = {'data':data_dict}
	
	data = json.dumps(data)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def grupo(request,id_grupo):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	contacto = Contactos.objects.using(database).filter(grupo_id=id_grupo).values('id','telefono','edad','nombre').order_by('-id')

	data_dict = ValuesQuerySetToDict(contacto)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")

@login_required(login_url="/ingresar")

def addgrupo(request):

	if request.method=='POST':

		id = request.user.id

		data=  json.loads(request.body)
		name = data['name']
		Grupo(name=name,user_id=id).save()

		return HttpResponse(name, content_type="application/json")

@login_required(login_url="/ingresar")

def uploadcontacto(request):

	if request.method=='POST':

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		archivo = request.FILES['process_file']

		grupo = request.POST['grupo']

		print 'grupo',grupo

		base = Excell(file=archivo).save(using=database)

		id_base = Excell.objects.using(database).all().values('id').order_by('-id')[0]['id']

		base = Excell.objects.using(database).get(id=id_base).file
	
		xls_name = '/var/www/html/'+str(base)

		book = xlrd.open_workbook(xls_name)

		sh = book.sheet_by_index(0)

		for rx in range(sh.nrows):

			for col in range(sh.ncols):

				destino = str(sh.row(rx)[col]).split(':')[1].split('.')[0]

				fecha = datetime.now()-timedelta(hours=5)

				print 'Saving...'+destino

				print grupo

				Contactos(telefono=destino,grupo_id=grupo).save(using=database)


		return HttpResponse(base, content_type="application/json")


@login_required(login_url="/ingresar")

def grupos(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	grupo = Grupo.objects.using(database).all().values('id','name').order_by('-id')

	data_dict = ValuesQuerySetToDict(grupo)	

	data = json.dumps(data_dict)

	if request.method == 'POST':

		print json.loads(request.body)

		data = json.loads(request.body)['dato']
		grupo=json.loads(request.body)['grupo']
		edad = data['edad']
		nombre = data['nombre']
		telefono = data['telefono']
	
		Contactos(edad=edad,nombre=nombre,telefono=telefono,grupo_id=grupo).save()

		return HttpResponse(nombre, content_type="application/json")

	return HttpResponse(data, content_type="application/json")

@login_required(login_url="/ingresar")
def audios(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	audio = Audios.objects.using(database).all().values('id','audio1','audio2').order_by('-id')

	data = ValuesQuerySetToDict(audio)	
	
	data = json.dumps(data)

	return HttpResponse(data, content_type="application/json")

@csrf_exempt
def uploadudioapi(request):

	if request.method == 'POST':

		data = request.POST

		print data

		#print  dict(data.iterlists())['name']

		request.FILES['audio']

		user='xiencias'
		psw='xiencias'

		user = authenticate(username=user, password=psw)

	
		if user is not None:

			if user.is_active:

				login(request, user)

				id=request.user.id

				database = AuthUser.objects.get(id=id).databases.name

				audio1 = request.FILES['audio']

				Audios(audio1=audio1,user_id=id).save(using=database)

				id_audio = Audios.objects.using(database).all().values('id').order_by('-id')[0]['id']

				audio = Audios.objects.using(database).get(id=id_audio)

				audio1 = str(audio.audio1).split('/')[1].replace('files/','')

				audio1 = audio1.split('.mp3')[0]

				os.system('sox /var/www/html/files/'+audio1+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio1+'.gsm')

				os.system('scp -P 5022 /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

				data = ValuesQuerySetToDict('audio')	
				
				data = json.dumps(data)

				return HttpResponse(data, content_type="application/json")
		else:

			data = json.dumps('User no valid')

			return HttpResponse(data, content_type="application/json")




@login_required(login_url="/ingresar")
def uploadaudio(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	audio1 = request.FILES['audio1']

	Audios(audio1=audio1,user_id=id).save(using=database)

	id_audio = Audios.objects.using(database).all().values('id').order_by('-id')[0]['id']

	audio = Audios.objects.using(database).get(id=id_audio)

	audio1 = str(audio.audio1).split('/')[1].replace('files/','')

	audio1 = audio1.split('.mp3')[0]

	os.system('sox /var/www/html/files/'+audio1+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio1+'.gsm')

	os.system('scp -P 5022 /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

	data = ValuesQuerySetToDict('audio')	
	
	data = json.dumps(data)

	return HttpResponse(data, content_type="application/json")



@login_required(login_url="/ingresar")
def campaniasms(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	campania = Campaniasms.objects.using(database).all().values('id','name','mensaje').order_by('-id')

	data = ValuesQuerySetToDict(campania)	
	
	data = json.dumps(data)

	return HttpResponse(data, content_type="application/json")

@login_required(login_url="/ingresar")
def campania(request):

	return render(request, 'campania.html',{})



@login_required(login_url="/ingresar")
def externalappedit(request):

	dato = json.loads(request.body)

	#{u'url': u'http://10.13.50.60/SUP/', u'nombre': u'SUP0', u'icono': u'shield', u'id': 1, u'servicio__name': u'SUP'}

	url = dato['url']
	nombre = dato['nombre']
	icono = dato['icono']
	id = dato['id']

	app = Externalapp.objects.get(id=id)
	
	app.url = url
	app.nombre = nombre
	app.icono = icono
	app.save()

	print dato

	return HttpResponse(nombre, content_type="application/json")

def aprobarvalidar(request,id):

	evento=Lote.objects.get(id=id)
	evento.aprobar=1
	evento.save()

	return HttpResponseRedirect("/eventodetalle/"+id)


@login_required(login_url="/ingresar")
def agregarcampania(request):

	print 'agregarcampania',json.loads(request.body)


	dato = json.loads(request.body)['dato']

	database = json.loads(request.body)['user']['databases__name']

	user = json.loads(request.body)['user']['id']

	mensaje = dato['mensaje']

	name = dato['namecampania']

	Campaniasms(name=name,mensaje=mensaje,user_id=user).save(using=database)

	return HttpResponse(name, content_type="application/json")

@login_required(login_url="/ingresar")
def verlotesms(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	data = Lote.objects.using(database).filter(servicio_id=5).values('id','name','fecha','aprobar','user','user__cliente__name').order_by('-id')

	fmt = '%Y-%m-%d %H:%M:%S %Z'

	for i in range(len(data)):

		data[i]['fecha'] = data[i]['fecha'].strftime(fmt)[0:19]


	data = ValuesQuerySetToDict(data)	
	
	data = json.dumps(data)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")
def smsindividual(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	data = json.loads(request.body)

	mensaje = data['mensaje']

	fecha = data['fecha']

	telefono = data['telefono']

	Traficosms(lote='SMS Individual',destino=telefono,mensaje=mensaje,status=2).save(using=database)

	return HttpResponse(mensaje, content_type="application/json")




@login_required(login_url="/ingresar")
def enviosms(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	dato =  json.loads(request.body)['dato']

	campania = dato['campanias']['id']

	name = dato['name']

	mensaje = dato['campanias']['mensaje']

	print 'mensaje',mensaje

	process_file = Grupo.objects.using(database).get(id=dato['grupo']['id']).excel.file
	
	xls_name = '/var/www/html/'+str(process_file)

	print xls_name

	book = xlrd.open_workbook(xls_name)

	sh = book.sheet_by_index(0)
	
	date =datetime.now()

	Lote(name=name,fecha=datetime.now(),aprobar=0,servicio_id=5,user_id=id,campania_id= campania).save(using=database)

	id_lote = Lote.objects.using(database).all().values('id').order_by('-id')[0]['id']

	sms = Lote.objects.using(database).get(id=id_lote).campania.mensaje

	a={}
	a1={}
	rx_ant = 0

	
	for rx in range(sh.nrows):

		if rx==0:

			for col in range(sh.ncols):

				a[col] = str(sh.row(rx)[col])
				a[col] = a[col].split(':')
				a[col] = a[col][1][1:20]
				a[col] = "%("+str(a[col])+")s"
				a[col] = a[col].replace("'","")	

		if rx > 0:

			smsx = sms

			for col in range(sh.ncols):

				a1[col] = str(sh.row(rx)[col])

				a1[col] = a1[col].split(':')

				a1[col]= a1[col][1][0:150]

			fono = a1[0]

			fono = fono.split('.')[0]

			fono = fono.replace("u'", "")

			fono = fono.replace("'","")

			print fono

			for col in range(sh.ncols):

				smsx = smsx.replace(a[col],a1[col])

				smsx = smsx.replace("u'","")

				smsx = smsx.replace("'","")

			print 'SMS',smsx

			Traficosms(lote_id=id_lote,destino=fono,mensaje=smsx,status=1).save(using=database)


	return HttpResponse(name, content_type="application/json")

@csrf_exempt
def apisms(request):

	if request.method == 'POST':

		dato = request.GET

		fecha = datetime.now()

		f = open('/var/www/html/apisms.txt', 'a')
		f.write(str(dato)+'_'+str(fecha)+'\n')
		f.close()

		usuario = dato['username']

		password = dato['password']

		numero = dato['phone_number']

		mensaje = dato['text_message']

		user = authenticate(username=usuario, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

			else:
				
				dato = 'Usuario no permitido'

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		proveedor = 'bulksms'
		# if usuario == 'cmyval':
		# 	proveedor='NA'

		print database

		if proveedor == 'smsc':

			dato = smsc(numero,cliente,mensaje)
	
		if proveedor == 'csnetworks':

			dato = csnetworks(numero,cliente,mensaje)
	
		if proveedor == 'infobip':

			audience = {numero:mensaje}

			print 'infobip',audience

			dato = infobip(audience)

		if proveedor == 'telintel':

			audience = {numero:mensaje}


			dato = telintel(audience)

		if proveedor == 'bulksms':

			audience = {numero:mensaje}

			dato = bulksms(audience)

		if proveedor == 'infobiplong':

			audience = {numero:mensaje}

			dato = infobiplong(audience)

		if proveedor == 'NA':

			dato = 'Pendiente por activar API SMS Cmyval comunicarse con Joel'

		fecha = datetime.now()

		if dato == 'OK' or dato =='Message sent to next instance' or dato == 'succeded':

			error = 0

		else:

			error = 1

		fecha = fecha -timedelta(hours=5)



		Traficosms(lote_id=1,destino=numero,mensaje=mensaje,status=3).save(using=database)

	
		return HttpResponse(dato, content_type="text/json")

	if request.method == 'GET':

		dato = request.GET

		fecha = datetime.now()

		f = open('/var/www/html/apismsget.txt', 'a')
		f.write(str(dato)+'_'+str(fecha)+'\n')
		f.close()

		usuario = dato['username']

		password = dato['password']

		numero = dato['phone_number']

		mensaje = dato['text_message']

		user = authenticate(username=usuario, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

			else:
				
				dato = 'Usuario no permitido'

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		proveedor = 'bulksms'
		# if usuario == 'cmyval':
		# 	proveedor='NA'

		
		if proveedor == 'smsc':

			dato = smsc(numero,cliente,mensaje)
	
		if proveedor == 'csnetworks':

			dato = csnetworks(numero,cliente,mensaje)
	
		if proveedor == 'infobip':

			audience = {numero:mensaje}

			print 'infobip',audience

			dato = infobip(audience)

		if proveedor == 'telintel':

			audience = {numero:mensaje}


			dato = telintel(audience)

		if proveedor == 'bulksms':

			audience = {numero:mensaje}

			print 'audience',audience

			dato = bulksms(audience)

			print dato

		if proveedor == 'infobiplong':

			audience = {numero:mensaje}

			dato = infobiplong(audience)

		if proveedor == 'NA':

			dato = 'Pendiente por activar API SMS Cmyval comunicarse con Joel'

		fecha = datetime.now()

		if dato == 'OK' or dato =='Message sent to next instance' or dato == 'succeded':

			error = 0

		else:

			error = 1

		fecha = fecha -timedelta(hours=5)



		Traficosms(lote_id=1,destino=numero,mensaje=mensaje,status=3).save(using=database)

	
		return HttpResponse(dato, content_type="text/json")

def enviarlotesms(request,id):

	database='MTC'

	evento=Lote.objects.using(database).get(id=id)
	fecha = datetime.now()
	fecha= fecha-timedelta(hours=5)
	evento.fecha = fecha
	evento.aprobar=1
	evento.estado=0

	os.environ['title']='Envio Campania SMS Xiencias'

	os.environ['body']='http://xiencias.com:9000/lotesms/'+str('xiencias')+'/'+str(id_lote)

	os.system('./b.sh')

	evento.save(using=database)

	return HttpResponse('dato', content_type="text/json")


@csrf_exempt
def enviarsms(request,id_lote):

	database='MTC'

	tt = Traficosms.objects.using(database).filter(lote_id=id_lote).count()

	te = Traficosms.objects.using(database).filter(lote_id=id_lote,status=2).count()

	if tt==te:

		e = Lote.objects.using(database).get(id=id_lote)

		e.estado = 1

		e.save()

	trafico = Traficosms.objects.using(database).filter(lote_id=id_lote,status=1)[:50]

	proveedor = 'bulksms'

	i = 0

	for t in trafico:

		print 'Enviando...',t.id,t.mensaje,t.destino

		id_sms = t.id

		mensaje = t.mensaje

		numero = t.destino

		sms = Traficosms.objects.using(database).get(id=id_sms)

		sms.status = 2

		sms.save()
		
		if proveedor == 'bulksms':

			audience = {numero:mensaje}

			dato = bulksms(audience)

			#dato ='OK'

		if dato == 'OK' or dato =='Message sent to next instance' or dato == 'succeded':
		
			error = 0

		else:
			
			error = 1

		print 'Proveedor.....',dato

		fecha = datetime.now()

		fecha= fecha-timedelta(hours=5)

		sms.reference = dato

		sms.error = error

		sms.reference_time = fecha

		sms.save()

		time.sleep(.500)


	return HttpResponse('Evento enviado'+str(id_lote), content_type="application/json")


@login_required(login_url="/ingresar")

def agregarlote(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	cliente = AuthUser.objects.get(id=id).cliente.id

	data = json.loads(request.body)['dato']

	encuesta = json.loads(request.body)['encuesta']


	if str(encuesta)=='True':

		encuesta = 1
	
	else:

		encuesta = 0


	print 'Encuesta......',encuesta



	grupo = data['grupo']['id']



	audio = data['audio']['id']

	audio = Audios.objects.using(database).get(id=audio)

	audio1 = str(audio.audio1)

	'''

	audio1 = str(audio.audio1).split('/')[1]

	audio1 = audio1.split('.mp3')[0]

	'''

	print '..................ACTIVAKkkkkkkkkkkkkk...............',audio1

	audiox = audio1.replace("files/","").replace(".mp3","")

	os.system('sox /var/www/html/files/'+audiox+'.mp3 -r 8000 -c1 /var/www/html/files/'+audiox+'.gsm')

	print 'sox /var/www/html/files/'+audiox+'.mp3 -r 8000 -c1 /var/www/html/files/'+audiox+'.gsm'

	os.system('scp -P 5022 /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

	# mf = mad.MadFile("/var/www/html/"+audio1)


	# duracion = mf.total_time()/1000

	duracion = None

	audiotxt = '1='+audio1

	name = data['name']

	fecha =datetime.now()

	contactos = Contactos.objects.using(database).filter(grupo_id=grupo)

	Lote(name= name,fecha=fecha,aprobar=0,servicio_id=1,user_id=id).save(using=database)

	id_lote = Lote.objects.using(database).all().values('id').order_by('-id')[0]['id']

	print ' Pushbullet sending ......'

	os.environ['title']='Envio Campania Voz Xiencias'

	os.environ['body']='http://xiencias.com:9000/lote/'+str(database)+'/'+str(id_lote)

	os.system('./b.sh')

	for c in contactos:

		destino = c.telefono

		audiotxt = audiotxt.replace('files/','').replace('.mp3','')

		DBlaster(duracion=duracion,lote_id=id_lote,destino=destino,audio=audiotxt,fh_inicio=fecha,lestado_id=0,oc7_2=0,cliente_id=int(cliente),tipo=3,dtmf=encuesta).save(using=database)

	audio = Audios.objects.using(database).all().values('id','audio1','audio2')

	data = ValuesQuerySetToDict(audio)	
	
	data = json.dumps(data)

	return HttpResponse(name, content_type="application/json")


@login_required(login_url="/ingresar")

def cancelarlote(request,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	dllam = DBlaster.objects.using(database).filter(lestado_id=0,lote=lote)

	for d in dllam:

		d.lestado_id = 5
		d.save()

	return HttpResponseRedirect("/lote/"+str(lote))


@login_required(login_url="/ingresar")
def enviarlote(request,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	dllam = DBlaster.objects.using(database).filter(lestado_id=5,lote=lote)

	for d in dllam:

		print d

		d.lestado_id = 0
		d.save()

	os.environ['title']='Envio Campania Voz Xiencias'

	os.environ['body']='http://xiencias.com:9000/lote/'+str(database)+'/'+str(id_lote)

	os.system('./b.sh')

	return HttpResponseRedirect("/lote/"+str(lote))




def bulksms(audience):

	url ="http://smsbulk.pe/SmsBulk/rest/ws/bulkSms"
	username = 'xiencias'
	password = '9nG4SB'


	for recipient in audience:
        
		phone_number = recipient

		message = audience[recipient]

		if phone_number[:2] != '51':

			phone_number = '51%s' % phone_number

		params = {'usr' : username,'pas' : password,'msg' : message ,'num' : phone_number}

		reply = requests.get(url, params=params)

		result1 = reply.text

		return result1

@login_required(login_url="/ingresar")
def uploadblaster(request):

	if request.method == 'POST':

		print request.FILES

		print request.POST


	return HttpResponse('dato', content_type="application/json")


@login_required(login_url="/ingresar")
def actualiza(request):

	id = request.user.id
	database = AuthUser.objects.get(id=id).databases.name

	b = DBlaster.objects.using(database).all()[:100]
	for i in b:


		if type(i.lote) != 'int': 

			print i.lote,i.id_d_blaster

			i.lote = Lote.objects.using(database).get(name=i.lote).id
			i.save(using=database)

			
	

	return HttpResponse('dato', content_type="application/json")



@login_required(login_url="/ingresar")
def csvfiltro(request):

	if request.method == 'POST':

		my_filter = {}

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		data = request.POST

		print 'Csv filtro......',data

		if data['lote'] != '?': 

			my_filter['id_d_blaster__lote__name'] = data['lote']

		if data['fechainicio'] != '':

			finicio = str(data['fechainicio'])[0:19]

			my_filter['t_pro__gte'] =finicio

		if data['fechafin'] != '':

			ffin = str(data['fechafin'])[0:19]

			my_filter['t_pro__lte'] =ffin

		resumen  = DLlamadas.objects.using(database).filter(**my_filter).values('id_d_llamadas','t_pro','d_total','audio','destino','id_d_blaster__lote','respuesta01')

		response = HttpResponse(content_type='text/csv')
		
		response['Content-Disposition'] = 'attachment; filename="Resumen.csv"'

		writer = csv.writer(response)

		writer.writerow(['Id','Fecha Proceso','Duracion de Llamada','Audio','Destino','Lote','Respuesta Encuesta'])

		for x in resumen:

			x['audio'] = x['audio'].encode('ascii','ignore')

			x['audio'] = x['audio'].encode('ascii','replace')

			x['destino'] = x['destino'].encode('ascii','ignore')

			x['destino'] = x['destino'].encode('ascii','replace')

			writer.writerow([x['id_d_llamadas'],x['t_pro'],x['d_total'],x['audio'],x['destino'],x['id_d_blaster__lote'],x['respuesta01']])
	   
		return response

@login_required(login_url="/ingresar")
def consulta(request):

	if request.method == 'POST':

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		data = json.loads(request.body)
		
		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in DBlaster.objects.using(database).raw("SELECT * FROM d_blaster order by id_d_blaster DESC"):

			d = collections.OrderedDict()
		
			d['id_d_blaster'] = row.id_d_blaster
			if row.fh_inicio:
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)

			llamada = DLlamadas.objects.using(database).filter(id_d_blaster=row.id_d_blaster)

			total = 0

			for l in llamada:

				con = l.d_total

				total = con + total 

				d['duracion'] = total
				d['intentos'] = l.vuelta
			
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			d['lestado'] = row.lestado.nombre
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			if row.tduracion:
				d['tduracion'] = row.tduracion.strftime(fmt)

	
			objects_list.append(d)

		dato = json.dumps(objects_list)
	

		return HttpResponse(dato, content_type="application/json")
		

@login_required(login_url="/ingresar")
def lanza(request):

	os.system("/opt/xien/lanza.sh")

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	print database

	llamadas = DLlamadas.objects.using(database).filter(flagfin=0)

	for l in llamadas:

		print 'Actualizando..'+str(l)

		l.flagfin = 1
		l.save()

	return HttpResponse('Sistema Activado :)', content_type="application/json")

@login_required(login_url="/ingresar")
def apaga(request):

	os.system("/opt/xien/apaga.sh")

	return HttpResponse('Sistema Apagado :(', content_type="application/json")


@login_required(login_url="/ingresar")
def querylote(request,database,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	fmt = '%Y-%m-%d %H:%M:%S %Z'

	voip = DLlamadas.objects.using(database).filter(id_d_blaster__lote=lote,flagfin=0).values('id_d_blaster','d_total','id_d_blaster__duracion','destino','id_d_blaster__lestado__nombre').order_by('-id_d_blaster__lestado__nombre')

	for i in range(len(voip)):

		voip[i]['fecha'] = DLlamadas.objects.using(database).get(id_d_blaster=voip[i]['id_d_blaster']).t_pro.strftime(fmt)[0:19]

	data_dict = ValuesQuerySetToDict(voip)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def querylotesms(request,database,lote,pagina):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	fmt = '%Y-%m-%d %H:%M:%S %Z'

	voip = Traficosms.objects.using(database).filter(lote_id=lote).values('id','lote','destino','mensaje','status').order_by('-id')[100*int(pagina):100*int(pagina) +100]

	data_dict = ValuesQuerySetToDict(voip)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def descargacsvlote(request,lote):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	voip = DLlamadas.objects.using(database).filter(id_d_blaster__lote=lote).values('id_d_blaster','d_total','id_d_blaster__duracion','destino','audio','t_pro','respuesta01')

	fmt = '%Y-%m-%d %H:%M:%S %Z'
		
	response = HttpResponse(content_type='text/csv')
	
	response['Content-Disposition'] = 'attachment; filename="'+lote+'.csv"'

	writer = csv.writer(response)

	writer.writerow(['ID','Duracion de Llamada','Duracion Audio','Destino','Audio','Fecha Proceso','Respuesta'])

	for x in voip:

		x['audio'] = x['audio'].encode('ascii','ignore')

		x['audio'] = x['audio'].encode('ascii','replace')

		x['destino'] = x['destino'].encode('ascii','ignore')

		x['destino'] = x['destino'].encode('ascii','replace')

		writer.writerow([x['id_d_blaster'],x['d_total'],x['id_d_blaster__duracion'],x['destino'],x['audio'],x['t_pro'],x['respuesta01']])
   
	return response
	



	
@login_required(login_url="/ingresar")
def consultalote(request):

	if request.method == 'POST':

		data = json.loads(request.body)

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		lote = data['lote']

		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in DBlaster.objects.using(database).raw("SELECT * FROM d_blaster where lote ='" + str(lote) + "'"):

			d = collections.OrderedDict()

			print row.lestado
		
			d['id_d_blaster'] = row.id_d_blaster
			d['lestado'] = row.lestado.nombre
			d['duracion'] = row.duracion
			print 'id',row.id_d_blaster

			llamada = DLlamadas.objects.using(database).filter(id_d_blaster=row.id_d_blaster)

			total = 0

			for l in llamada:

				con = l.d_total

				total = con + total 

				d['duracionllamada'] = total
				d['intentos'] = l.vuelta

			if row.fh_inicio:
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)
			d['lote'] = row.lote
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			

	
			objects_list.append(d)

		j = json.dumps(objects_list)


		return HttpResponse(j, content_type="application/json")


@csrf_exempt
def consultablaster(request,id_blaster):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	fmt = '%Y-%m-%d %H:%M:%S %Z'

	objects_list = []

	for row in DBlaster.objects.using(database).raw("SELECT fh_inicio,tduracion_ini,tduracion_fin,tduracion,id_d_blaster,uid,destino,audio,derivacion,lestado,respuesta,dtmf,despedida,oc7_1,oc7_2,oc7_3 FROM d_blaster where id_d_blaster ='" + str(id_blaster) + "'"):

		d = collections.OrderedDict()
		
		d['id_d_blaster'] = row.id_d_blaster
		d['fh_inicio'] = row.fh_inicio.strftime(fmt)
		d['uid'] = row.uid
		d['destino'] = row.destino
		d['audio'] = row.audio
		d['derivacion'] = row.derivacion
		d['lestado'] = row.lestado
		d['respuesta'] = row.respuesta
		d['dtmf'] = row.dtmf
		d['despedida'] = row.despedida
		d['oc7_1'] = row.oc7_1
		d['oc7_2'] = row.oc7_2
		d['oc7_3'] = row.oc7_3
		if row.tduracion_ini:
			d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
		if row.tduracion_fin:
			d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
		if row.tduracion:
			d['tduracion'] = row.tduracion.strftime(fmt)


		objects_list.append(d)

	j = json.dumps(objects_list)


	return HttpResponse(j, content_type="application/json")


@csrf_exempt
def verlote(request):

	id = request.user.id

	print id

	database = AuthUser.objects.get(id=id).databases.name

	print 'Database',database

	lotes= Lote.objects.using(database).all().values('id','name','estado').order_by('-id')[:50]

	fmt = '%Y-%m-%d %H:%M:%S %Z'

	for i in range(len(lotes)):

		

		print 'data', lotes[i]['id']


		lotes[i]['fecha'] = Lote.objects.using(database).get(id=lotes[i]['id']).fecha.strftime(fmt).replace('UTC','')

		lotes[i]['porenviar'] = DBlaster.objects.using(database).filter(lote=str(lotes[i]['id']),lestado=0).count()
		lotes[i]['enviado'] = DBlaster.objects.using(database).filter(lote=str(lotes[i]['id']),lestado=1).count()
		


	data_dict = ValuesQuerySetToDict(lotes)

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


def pushin(request):

	print request.POST 

	if request.user.is_authenticated():

		return HttpResponseRedirect("/menu")

	else:

		if request.method == 'POST':

			
			print request.POST


			user = request.POST['user']
			
			psw = request.POST['password']

			user = authenticate(username=user, password=psw)

		
			if user is not None:

				if user.is_active:

					login(request, user)

					if user == 'root':

						return HttpResponseRedirect("/menu")

					else:

						return HttpResponseRedirect("/menu")

			else:

				return HttpResponseRedirect("/ingresar")
		
		else:

			return render(request, 'ingresar.html',{})


def index(request):

	return render(request, 'index.html',{})

def ingresar(request):

	return render(request, 'ingresar.html',{})


@login_required(login_url="/ingresar")
def audiocarga(request):

	if request.method == 'POST':

		audio1 = request.FILES['audio1']
		audio2 = request.FILES['audio2']

	return render(request, 'audiocarga.html',{})

@login_required(login_url="/ingresar")
def usuario(request):

	return render(request, 'usuario.html',{})

@login_required(login_url="/ingresar")
def descargacsv(request):


	return render(request, 'csv.html',{})




@login_required(login_url="/ingresar")
def reporte(request):

	return render(request, 'reporte.html',{})


@login_required(login_url="/ingresar")
def introduccion(request):

	return render(request, 'introduccion.html',{})


@login_required(login_url="/ingresar")
def audio(request):

	return render(request, 'audio.html',{})

@login_required(login_url="/ingresar")
def run(request):

	return render(request, 'run.html',{})


@login_required(login_url="/ingresar")
def menud(request):

	return render(request, 'menud.html',{})

@login_required(login_url="/ingresar")
def filtros(request):

	return render(request, 'filtros.html',{})

@login_required(login_url="/ingresar")
def mail(request):

	return render(request, 'mail.html',{})


@login_required(login_url="/ingresar")
def externalapp(request):

	return render(request, 'externalapp.html',{})


@login_required(login_url="/ingresar")
def agenda(request):

	return render(request, 'agenda.html',{})



@login_required(login_url="/ingresar")
def introduccion(request):

	return render(request, 'introduccion.html',{})


@login_required(login_url="/ingresar")
def docconsulta(request):

	return render(request, 'docconsulta.html',{})

@login_required(login_url="/ingresar")
def doccarga(request):

	return render(request, 'doccarga.html',{})


@login_required(login_url="/ingresar")
def sms(request):

	return render(request, 'sms.html',{})


@login_required(login_url="/ingresar")
def sup(request):

	return render(request, 'sup.html',{})

@login_required(login_url="/ingresar")
def age(request):

	return render(request, 'age.html',{})


def inicio(request):

	return render(request, 'inicio.html',{})

@login_required(login_url="/ingresar")
def configuracion(request):

	return render(request, 'configuracion.html',{})



@login_required(login_url="/ingresar")
def lote(request,database,nombre):


	return render(request, 'lote.html',{'nombre':nombre,'name':database})

@login_required(login_url="/ingresar")
def lotesms(request,database,nombre):

	name = nombre.replace("_"," ")

	return render(request, 'lotesms.html',{'nombre':nombre,'name':name})


@login_required(login_url="/ingresar")
def mlote(request):
	return render(request, 'mlote.html',{})


@login_required(login_url="/ingresar")
def servicio(request):
	return render(request, 'servicio.html',{})

@login_required(login_url="/ingresar")
def cargabase(request):
	return render(request, 'base.html',{})

@login_required(login_url="/ingresar")
def menu(request):
	return render(request, 'menu.html',{})

@login_required(login_url="/ingresar")
def cliente(request):
	return render(request, 'cliente.html',{})





def salir(request):

	logout(request)
	
	return HttpResponseRedirect("/")


@login_required(login_url="/ingresar")

def clientes(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).cliente.database.name

	database_id = AuthUser.objects.get(id=id).cliente.database.id

	grupo = User.objects.get(id=id).groups.get()

	cliente = AuthUser.objects.get(id=id).cliente.id

	print grupo,database

	if str(grupo) == 'Admin':

		clientes = Clientes.objects.all().values('id','database__name','name','database','capa')

	if str(grupo) == 'Superuser':

		clientes = Clientes.objects.filter(database__name=database,capa=2).values('id','database__name','name','database','capa')

	if str(grupo) == 'Manager':

		clientes = Clientes.objects.filter(id=cliente).values('id','database__name','name','database','capa')


	print 'clientes',clientes

	data_dict = ValuesQuerySetToDict(clientes)	

	clientes = json.dumps(data_dict)

	if request.method == 'POST':

		data = json.loads(request.body)

		clientes = str(data['name'])

		if str(grupo) == 'Superuser':

			Clientes(database_id=database_id,capa=2,name=data['name']).save()


	return HttpResponse(clientes, content_type="application/json")


@login_required(login_url="/ingresar")

def user(request):

	id = request.user.id

	clientes = AuthUser.objects.filter(id=id).values('id','username','first_name','databases','databases__name','cliente__name','cliente__capa','authusergroups__group_id__name')

	data_dict = ValuesQuerySetToDict(clientes)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def appexternas(request):

	id = request.user.id

	clientes = Externalapp.objects.using('default').all().values('id','url','nombre','icono','servicio__name')

	data_dict = ValuesQuerySetToDict(clientes)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")

@login_required(login_url="/ingresar")

def blasterindividual(request):

	id = request.user.id

	cliente = AuthUser.objects.get(id=id).cliente.id

	database = AuthUser.objects.get(id=id).cliente.database.name

	if request.method == 'POST':

		data = json.loads(request.body)

		print data

		fecha = data['fecha']

		audio = str(data['audio']['audio1']).split('.mp3')[0].replace('files/','')

		destino = str(data['destino'])

		#{u'fecha': u'2016-01-01', u'audio': {u'id': 97, u'audio2': u'', u'audio1': u'prueba.mp3'}, u'name': u'980729468'}

		DBlaster(lote='Blaster Individual',destino=destino,audio='1='+str(audio),fh_inicio=fecha,lestado_id=0,oc7_2=0,cliente_id=cliente,tipo=3).save(using=database)
	
		print audio

	return HttpResponse(audio, content_type="application/json")


@login_required(login_url="/ingresar")

def externaladd(request):

	id = request.user.id

	if request.method == 'POST':

		data = json.loads(request.body)

		url = data['url']

		nombre = data['nombre']

		icono=data['icono']

		Externalapp(url=url,nombre=nombre,icono=icono).save()

	return HttpResponse(nombre, content_type="application/json")



@login_required(login_url="/ingresar")

def usercliente(request,id_cliente):


		usuarios = AuthUser.objects.filter(cliente_id=id_cliente).values('id','username','first_name','databases__name','authusergroups__group_id__name')

		data_dict = ValuesQuerySetToDict(usuarios)

		data = json.dumps(data_dict)

		return HttpResponse(data, content_type="application/json")

def userclientecliente(request,id_cliente):

	if request.method == 'GET':

		id = request.user.id

		usuarios = AuthUser.objects.filter(cliente_id=id_cliente).values('id','username','first_name','databases__name','authusergroups__group_id__name')

		data_dict = ValuesQuerySetToDict(usuarios)

		data = json.dumps(data_dict)

		return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def clientecliente(request,id_cliente,id_database):

	id = request.user.id

	database = AuthUser.objects.get(id=id).cliente.name

	grupo = User.objects.get(id=id).groups.get()

	print grupo

	cliente = Clientes.objects.filter(database_id=id_database,capa=1).values('id','name','database__name')

	data_dict = ValuesQuerySetToDict(cliente)

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")



@login_required(login_url="/ingresar")

def usuarios(request):

	if request.method == 'GET':

		id = request.user.id

		cliente = AuthUser.objects.get(id=id).cliente.id

		database = AuthUser.objects.get(id=id).cliente.database.name

		grupo = User.objects.get(id=id).groups.get()

		print database

		if str(grupo) == 'Admin':

			usuarios = AuthUser.objects.all().values('id','username','first_name','cliente__database__name','authusergroups__group_id__name','cliente__name')

		if str(grupo) == 'Superuser':

			usuarios = AuthUser.objects.filter(cliente__database__name=database).values('id','username','first_name','cliente__database__name','authusergroups__group_id__name','cliente__name')

		if str(grupo) == 'Manager':

			usuarios = AuthUser.objects.filter(cliente=cliente).values('id','username','first_name','cliente__database__name','authusergroups__group_id__name','cliente__name')

		data_dict = ValuesQuerySetToDict(usuarios)	

		data = json.dumps(data_dict)

		return HttpResponse(data, content_type="application/json")

	
	if request.method == 'POST':

		data = json.loads(request.body)

		print data

		cliente = data['cliente']['id']

		username = data['user']['username']

		first_name = data['user']['first_name']

		password = data['user']['password']

		grupo = data['user']['selected']['id']

		user = User.objects.create_user(username=username,password=password)

		if grupo == 1:

			user.groups.add(3) 

		if grupo == 2:

			user.groups.add(4) 

		user.save()

		id_user = AuthUser.objects.all().values('id').order_by('-id')[0]['id']

		u = AuthUser.objects.get(id=id_user)

		u.cliente_id = cliente

		u.first_name = first_name

		u.save()


		return HttpResponse(username, content_type="application/json")


	




@login_required(login_url="/ingresar")

def servicios(request,id_user):

	id = request.user.id



	clientes = Serviciouser.objects.using('default').filter(user=id_user).values('id','servicio__name','status','servicio_id')

	data_dict = ValuesQuerySetToDict(clientes)	

	data = json.dumps(data_dict)

	if request.method == 'POST':

		data = json.loads(request.body)

		name = data['servicio']['servicio__name']

		servicio = data['servicio']['servicio_id']

		id_user = data['user']

		Serviciouser(servicio_id=servicio,user_id=id_user).save()

		return HttpResponse(name, content_type="application/json")

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def activar(request,id_serviciouser):

	id = request.user.id

	servicio = Serviciouser.objects.using('default').get(id=id_serviciouser)

	servicio.status = 1

	servicio.save()

	return HttpResponse(servicio.user.first_name, content_type="application/json")

@login_required(login_url="/ingresar")

def desactivar(request,id_serviciouser):

	id = request.user.id

	servicio = Serviciouser.objects.using('default').get(id=id_serviciouser)

	servicio.status = 0

	servicio.save()


	return HttpResponse(servicio.user.first_name, content_type="application/json")


@login_required(login_url="/ingresar")

def infolote(request,id):

	id = request.user.id

	lote = Lote.objects.filter(id=id).values('id','name')
	
	data_dict = ValuesQuerySetToDict(lote)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")


@login_required(login_url="/ingresar")

def serviciosapi(request):

	id = request.user.id

	servicio = Serviciouser.objects.using('default').filter(user_id=id).values('id','user__first_name','servicio__name','status').order_by('servicio__name')

	data_dict = ValuesQuerySetToDict(servicio)	

	data = json.dumps(data_dict)

	return HttpResponse(data, content_type="application/json")



def upbase(request):

	id = request.user.id

	database = AuthUser.objects.get(id=id).databases.name

	grupo = request.POST['name']

	base = request.FILES['process_file']

	Excell(file=base).save(using=database)

	id_base = Excell.objects.using(database).all().values('id').order_by('-id')[0]['id']

	base = Excell.objects.using(database).get(id=id_base).file

	print 'iiii',id

	Grupo(name=grupo,excel_id= id_base,user_id=id).save(using=database)

	id_grupo = Grupo.objects.using(database).all().values('id').order_by('-id')[0]['id']

	xls_name = '/var/www/html/'+str(base)

	print xls_name

	book = xlrd.open_workbook(xls_name)

	sh = book.sheet_by_index(0)

	a1={}

	for rx in range(sh.nrows):

		for col in range(sh.ncols):


			a1[col] = str(sh.row(rx)[col])

			a1[col] = a1[col].split(':')

			a1[col]= a1[col][1][0:150]


		destino = a1[0].split('.')[0]
	
		Contactos(telefono=destino,grupo_id=id_grupo).save(using=database)

	
	return HttpResponseRedirect("/mlote/")




@login_required(login_url="/ingresar")

def lotes(request):

		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name

		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in Lote.objects.using(database).raw("SELECT id,name,fecha,aprobar FROM lote order by id DESC "):

			d = collections.OrderedDict()
			d['id'] = row.id
			d['name'] = row.name

			if row.fecha :

				d['fecha'] = row.fecha.strftime(fmt)
			
			d['aprobar'] = row.aprobar

			objects_list.append(d)

		j = json.dumps(objects_list)


		return HttpResponse(j, content_type="application/json")


@login_required(login_url="/ingresar")

def voipsingle(request,id_serviciouser):

	if request.method == 'POST':

			data = json.loads(request.body)

			print data

			username = data['username']

			password = data['password']

			id_lote = data['lote']

			user = authenticate(username=username, password=password)

			if user is not None:

				if user.is_active:

					login(request, user)

				else:
					
					dato = 'Usuario no permitido'


			id = request.user.id

			database = AuthUser.objects.get(id=id).databases.name

			fmt = '%Y-%m-%d %H:%M:%S %Z'

			objects_list = []

			for row in DBlaster.objects.using(database).raw("SELECT lote,fh_inicio,tduracion_ini,tduracion_fin,tduracion,id_d_blaster,uid,destino,audio,derivacion,lestado,respuesta,dtmf,despedida,oc7_1,oc7_2,oc7_3 FROM d_blaster where lote ='" + str(id_lote) + "'"):

				d = collections.OrderedDict()
			
				d['id_d_blaster'] = row.id_d_blaster
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)
				d['lote'] = row.lote.name
				d['destino'] = row.destino
				d['audio'] = row.audio
				d['derivacion'] = row.derivacion
				d['lestado'] = row.lestado
				d['respuesta'] = row.respuesta
				d['dtmf'] = row.dtmf
				d['despedida'] = row.despedida
				d['oc7_1'] = row.oc7_1
				d['oc7_2'] = row.oc7_2
				d['oc7_3'] = row.oc7_3
				if row.tduracion_ini:
					d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
				if row.tduracion_fin:
					d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
				if row.tduracion:
					d['tduracion'] = row.tduracion.strftime(fmt)

		
				objects_list.append(d)

			j = json.dumps(objects_list)


			return HttpResponse(j, content_type="application/json")


def uploadbase(request):

		if request.method == 'POST':

			id = request.user.id

			database = AuthUser.objects.get(id=id).databases.name

			cliente = AuthUser.objects.get(id=id).cliente.id

			archivo = request.FILES['process_file']

			audio1 = request.FILES['audio1']

			nombre = str(request.POST['nombre']).replace(" ", "_")
		
			myDict = dict(request.POST.iterlists())

			encuesta = 0

			for elem in myDict:

				if elem ==  'check':

					check = request.POST['check']

					if check == 'true':

						audio2 = request.FILES['audio2']

						Audios(audio1=audio1,audio2=audio2).save(using=database)

						sincheck = 1

					if check == 'false':

						Audios(audio1=audio1).save(using=database)

				else:

					sincheck = 0

				if elem == 'encuesta':

					encuesta = 1


			print 'encuesta',encuesta


			if sincheck == 0:

				Audios(audio1=audio1).save(using=database)


			id_audio = Audios.objects.using(database).all().values('id').order_by('-id')[0]['id']

			audio = Audios.objects.using(database).get(id=id_audio)

			audio1 = str(audio.audio1).split('/')[1].replace('files/','')

			audio1 = audio1.split('.mp3')[0]

			os.system('sox /var/www/html/files/'+audio1+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio1+'.gsm')

			os.system('scp -P 5022 /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

			mf = mad.MadFile("/var/www/html/"+audio1+".mp3")

			duracion = mf.total_time()/1000

			#rsync -avz -e "ssh -p 5022" root@xiencias.com:/var/www/html/files/ /etc/asterisk/voces/


			if sincheck == 1:

				audio2 = str(audio.audio2).split('/')[1].replace('files/','')

				audio2 = audio2.split('.mp3')[0]

				os.system('sox /var/www/html/files/'+audio2+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio2+'.gsm')

				os.system('scp -P 5022 /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

				os.system('scp /var/www/html/files/*.gsm root@10.13.50.100:/etc/asterisk/voces/')

				audiotxt= "1="+audio1+"|2="+audio2

			if sincheck == 0:

				audiotxt= "1="+audio1


			baseh = Excell(file=archivo).save(using=database)

			print database

			id_baseh = Excell.objects.using(database).all().values('id').order_by('-id')[0]['id']

			base = Excell.objects.using(database).get(id=id_baseh).file
		
			xls_name = '/var/www/html/'+str(base)

			book = xlrd.open_workbook(xls_name)

			sh = book.sheet_by_index(0)

			for rx in range(sh.nrows):

				for col in range(sh.ncols):

					destino = str(sh.row(rx)[col]).split(':')[1].split('.')[0]

					fecha = datetime.now() - timedelta(hours=5)

					audiotxt = audiotxt.replace("files/","")

					DBlaster(duracion=duracion,lote=nombre,destino=destino,audio=audiotxt,fh_inicio=fecha,lestado_id=0,oc7_2=0,cliente_id=cliente,tipo=3,dtmf=encuesta).save(using=database)
	
			Lote(name= nombre,fecha=fecha,aprobar=0).save(using=database)

			j={'database':database,'nombre':nombre}

			j = json.dumps(j)

			return HttpResponse(j, content_type="application/json")



def buscar(request):

	if request.method == 'POST':


		filtro = request.POST

		

		fmt = '%Y-%m-%d %H:%M:%S %Z'
		inicio ='2000-01-01'
		fin = '4000-01-01'
		elemento = ''
		valor = ''

		for i in list(filtro):

			if i == 'inicio':

				inicio = filtro['inicio']
				inicio = str(inicio)

			if i == 'fin':

				fin = filtro['fin']
				fin = str(fin)
				
			if i == 'parametro':

				elemento = filtro['parametro']

			if i == 'valor':
				
				valor = filtro['valor']

			
		inicio = datetime.strptime(inicio, "%d %B, %Y")
		fin = datetime.strptime(fin, "%d %B, %Y")
		objects_list = []

		con =0

		print '...........',elemento,valor

		if elemento != '' and valor != '':

			query = "SELECT * FROM d_blaster where  fh_inicio >='" + str(inicio) + "' and fh_inicio <= '" + str(fin) + "' and " + elemento + " = '"+ valor +"' ORDER BY id_d_blaster DESC"

		else:

			query ="SELECT * FROM d_blaster where  fh_inicio >='" + str(inicio) + "' and fh_inicio <= '" + str(fin) + "' ORDER BY id_d_blaster DESC"
		
		id = request.user.id

		database = AuthUser.objects.get(id=id).databases.name


		for row in DBlaster.objects.using(database).raw(query):

			d = collections.OrderedDict()
			
			d['id_d_blaster'] = row.id_d_blaster
			d['fh_inicio'] = row.fh_inicio.strftime(fmt)
			d['lote'] = row.lote
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			d['lestado'] = row.lestado.nombre
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			if row.tduracion:
				d['tduracion'] = row.tduracion.strftime(fmt)

	
			objects_list.append(d)
			con=con+1

			

		j={'data':objects_list,'con':con}
		j = json.dumps(j)

		return HttpResponse(j, content_type="application/json")
	
@csrf_exempt
def audioapi(request):

	if request.method == 'POST':

		username = request.POST['username']

		password = request.POST['username']

		destino =request.POST['destino']

		audio = request.POST['audio']

		user = authenticate(username=username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

				id = request.user.id

				database = AuthUser.objects.get(id=id).databases.name

				x=os.system('sox /var/www/html/files/'+audio+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio+'.gsm')

				if int(x)==512:

					dato = json.dumps('Audio no encontrado')

					return HttpResponse(dato, content_type="application/json")

				os.system('scp  /var/www/html/files/*.gsm root@192.241.170.39:/etc/asterisk/voces/')

				audiotxt= "1="+audio

				fecha = datetime.now()

				audiotxt = audiotxt.replace('files/','')

				DBlaster(lote_id=136,destino=destino,audio=audiotxt,fh_inicio=fecha,lestado_id=0,oc7_2=0,cliente_id=3,tipo=3).save(using=database)

				dato = json.dumps('API VOZ Enviado')

				return HttpResponse(dato, content_type="application/json")
		

		else:
				
				dato = 'Usuario no permitido'

				return HttpResponse(dato, content_type="application/json")




@csrf_exempt
def blaster(request):

	if request.method == 'POST':

		auth = request.POST['auth']

		print request.FILES

		auth = base64.b64decode(auth)

		username = auth.split(':')[0]

		password = auth.split(':')[1]

		user = authenticate(username=username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

				id = request.user.id

				database = AuthUser.objects.get(id=id).databases.name

		else:
				
				dato = 'Usuario no permitido'


		archivo = request.FILES['base']

		audio1 = request.FILES['audio1']

		nombre = str(request.POST['nombre']).replace(" ", "_")

		myDict = dict(request.POST.iterlists())

		print 'database',database

		Audios(audio1=audio1).save(using=database)

		id_audio = Audios.objects.using(database).all().values('id').order_by('-id')[0]['id']

		audio = Audios.objects.using(database).get(id=id_audio)

		audio1 = str(audio.audio1).split('/')[1]

		audio1 = audio1.split('.mp3')[0]

		f = open('/var/www/html/log.html','w')

		f.write('LOG Apps ')

		f.write('sox /var/www/html/files/'+audio1+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio1+'.gsm')

		f.close()
    
		os.system('sox /var/www/html/files/'+audio1+'.mp3 -r 8000 -c1 /var/www/html/files/'+audio1+'.gsm')

		os.system('scp  /var/www/html/files/*.gsm root@10.13.50.100:/etc/asterisk/voces/')
		
		audiotxt= "1="+audio1

		baseh = Excell(file=archivo).save(using=database)

		print database

		id_baseh = Excell.objects.using(database).all().values('id').order_by('-id')[0]['id']

		base = Excell.objects.using(database).get(id=id_baseh).file
	
		xls_name = '/var/www/html/'+str(base)

		book = xlrd.open_workbook(xls_name)

		sh = book.sheet_by_index(0)

	
		for rx in range(sh.nrows):

			for col in range(sh.ncols):


				destino = str(sh.row(rx)[col]).split(':')[1].split('.')[0]

				fecha = datetime.now()

				audiotxt = audiotxt.replace('files/','')

				DBlaster(lote=nombre,destino=destino,audio=audiotxt,fh_inicio=fecha,lestado_id=0,oc7_2=0,cliente_id=3,tipo=3).save(using=database)


		
		return HttpResponse('ok', content_type="application/json")



@csrf_exempt
def consultablaster(request):

	if request.method == 'POST':


		auth = request.POST['auth']

		auth = base64.b64decode(auth)

		username = auth.split(':')[0]

		password = auth.split(':')[1]

		user = authenticate(username=username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

				id = request.user.id

				database = AuthUser.objects.get(id=id).databases.name

		else:
				
				dato = 'Usuario no permitido'


		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in DBlaster.objects.using(database).raw("SELECT * FROM d_blaster "):

			d = collections.OrderedDict()
		
			d['id_d_blaster'] = row.id_d_blaster
			if row.fh_inicio:
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)
			
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			d['lestado'] = row.lestado.nombre
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			if row.tduracion:
				d['tduracion'] = row.tduracion.strftime(fmt)

	
			objects_list.append(d)

		dato = json.dumps(objects_list)
	

		return HttpResponse(dato, content_type="application/json")


@csrf_exempt
def consultaloteblaster(request):

	if request.method == 'POST':

		auth = request.POST['auth']

		lote = request.POST['lote']

		auth = base64.b64decode(auth)

		username = auth.split(':')[0]

		password = auth.split(':')[1]

		user = authenticate(username=username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

				id = request.user.id

				database = AuthUser.objects.get(id=id).databases.name

		else:
				
				dato = 'Usuario no permitido'

		lote = request.POST['lote']

		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in DBlaster.objects.using(database).raw("SELECT * FROM d_blaster where lote ='" + str(lote) + "'"):

			d = collections.OrderedDict()

			print row.lestado
		
			d['id_d_blaster'] = row.id_d_blaster
			d['lestado'] = row.lestado.nombre

			print 'id',row.id_d_blaster

			llamada = DLlamadas.objects.using(database).filter(id_d_blaster=row.id_d_blaster)

			total = 0

			for l in llamada:

				con = l.d_total

				total = con + total 

				d['duracion'] = total
				d['intentos'] = l.vuelta

			if row.fh_inicio:
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)
			d['lote'] = row.lote
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			

	
			objects_list.append(d)

		j = json.dumps(objects_list)


		return HttpResponse(j, content_type="application/json")


@csrf_exempt
def lotesblaster(request):

	if request.method == 'POST':

		auth = request.POST['auth']

		lote = request.POST['lote']

		auth = base64.b64decode(auth)

		username = auth.split(':')[0]

		password = auth.split(':')[1]

		user = authenticate(username=username, password=password)

		if user is not None:

			if user.is_active:

				login(request, user)

				id = request.user.id

				database = AuthUser.objects.get(id=id).databases.name

		else:
				
				dato = 'Usuario no permitido'

		lote = request.POST['lote']

		fmt = '%Y-%m-%d %H:%M:%S %Z'

		objects_list = []

		for row in DBlaster.objects.using(database).raw("SELECT * FROM d_blaster where lote ='" + str(lote) + "'"):

			d = collections.OrderedDict()

			print row.lestado
		
			d['id_d_blaster'] = row.id_d_blaster
			d['lestado'] = row.lestado.nombre

			print 'id',row.id_d_blaster

			llamada = DLlamadas.objects.using(database).filter(id_d_blaster=row.id_d_blaster)

			total = 0

			for l in llamada:

				con = l.d_total

				total = con + total 

				d['duracion'] = total
				d['intentos'] = l.vuelta

			if row.fh_inicio:
				d['fh_inicio'] = row.fh_inicio.strftime(fmt)
			d['lote'] = row.lote
			d['destino'] = row.destino
			d['audio'] = row.audio
			d['derivacion'] = row.derivacion
			
			d['respuesta'] = row.respuesta
			d['dtmf'] = row.dtmf
			d['despedida'] = row.despedida
			d['oc7_1'] = row.oc7_1
			d['oc7_2'] = row.oc7_2
			d['oc7_3'] = row.oc7_3
			if row.tduracion_ini:
				d['tduracion_ini'] = row.tduracion_ini.strftime(fmt)
			if row.tduracion_fin:
				d['tduracion_fin'] = row.tduracion_fin.strftime(fmt)
			

	
			objects_list.append(d)

		j = json.dumps(objects_list)


		return HttpResponse(j, content_type="application/json")


