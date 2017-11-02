import requests
import json
#YmV5b25kOjEyMw==


url ="http://localhost:8000/consulta/"
params = {'auth':'YmV5b25kOjEyMw=='}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(params), headers=headers)


f = open('/var/www/html/consulta.html','w')
f.write(r.text)
f.close()
