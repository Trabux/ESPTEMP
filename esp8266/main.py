import machine
import time
import ujson
from constants import SERVER, ALARM_PIN 
from lib0 import *
####################################################################
#Metodo per entrare in deepsleep per msec secondi###################
####################################################################
def deep_sleep(msecs):
  # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
    rtc.alarm(rtc.ALARM0, msecs)

  # put the device to sleep
    machine.deepsleep()
####################################################################

vAlarm=ALARM_PIN #variabile pin da constants

alarm = machine.Pin(vAlarm, machine.Pin.OUT) #settaggio pin allarme

alarm.value(0) # settaggio allarme a 0

do_connect() #connetti wifi Station

vserver=SERVER #indirizzo server a cui mandare i dati

dati=leggi_sensore() #recupera temperature con controllo allarme

jdati=ujson.loads(dati) #trasforma in json

print(dati) #debug seriale

req = post(vserver + "/dati.php",data=None,json=jdati) #invia dati al server

print(req.text) #debug seriale
print("deepsleep tra 1,5 secondi") #debug seriale

time.sleep_ms(750) #aspetta

time.sleep_ms(750) #aspetta

deep_sleep(30000) #deep sleep 30s