import MySQLdb
import requests
import datetime
import json
import time


while True :

    time.sleep(6)

    fechanow = datetime.datetime.now() 

    db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="d4t4B4$3*",db="MTC") 

    cur = db.cursor()

    cur.execute("SELECT id,aprobar FROM lote where estado = %s and fecha <= %s and aprobar = %s ", 
    (0, fechanow,1))  

    y = cur.fetchall()

    print y

    lote = [item for item in y]

    
    for e in lote:

        r = requests.get('http://xiencias.com:9000/enviarsms/'+str(e[0]))

        f = open('/var/www/html/evento.html','w')

        f.write('Eventos')

        f.write(r.text)

        f.close()

    
            
