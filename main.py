import ujson
#import esp
#esp.osdebug(None)
import gc
import usocket
from constants import SERVER
from lib0 import *



do_connect()
#vterra=0.0
#vmezza=0.0
#valto=0.0
#SERVER=input("Inseririsci indirizzo Server: ")
vserver=SERVER
#gestione webserver
#s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
#s.bind(('', 80))
#s.listen(5)

while True:
    time.sleep_ms(750)
    time.sleep_ms(750)
    dati=leggi_sensore()
#    dati='{"terra": ' + str(vterra) + '  ,   "mezza":  ' + str(vmezza) + '  ,  "alto": ' + str(valto) + '}'
    jdati=ujson.loads(dati)
    print(dati)
    req = post("http://" + vserver + "/dati.php",data=None,json=jdati)
    print(req.text)
    time.sleep_ms(750)
    time.sleep_ms(750)