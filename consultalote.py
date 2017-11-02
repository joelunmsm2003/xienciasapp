import requests

url ="http://localhost:8000/consultalote/"
params = {'username':'root','password':'123','lote':'1'}
r=requests.post(url,params=params)


print r.text


f = open('/var/www/html/consultalote.html','w')
f.write(r.text)
f.close()
