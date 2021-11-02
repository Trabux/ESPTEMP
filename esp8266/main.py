import ujson
#import esp
#esp.osdebug(None)
import usocket
from constants import SERVER
from lib0 import *

#connetti wifi Station
do_connect()

#indirizzo server a cui mandare i dati
vserver=SERVER
while True:
    time.sleep_ms(750)
    time.sleep_ms(750)
    dati=leggi_sensore()
    jdati=ujson.loads(dati)
    print(dati)
    req = post("http://" + vserver + "/dati.php",data=None,json=jdati)
    print(req.text)
    time.sleep_ms(750)
    time.sleep_ms(750)