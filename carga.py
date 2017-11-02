import requests
import json
#root cm9vdDoxMjM=


fonos = ['980729169','980729691']
fonos = json.dumps(fonos)

url ="http://localhost:8000/carga/"
params = {'fono': fonos ,'auth':'cm9vdDoxMjM='}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(params), headers=headers)


f = open('/var/www/html/consulta.html','w')
f.write(r.text)
f.close()
