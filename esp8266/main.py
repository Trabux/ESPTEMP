import machine
from machine import Pin
from time import sleep, sleep_ms
import ujson

#import esp
#esp.osdebug(None)
import usocket

from constants import SERVER, LED 
from lib0 import *


def deep_sleep(msecs):
  # configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
  rtc.alarm(rtc.ALARM0, msecs)

  # put the device to sleep
  machine.deepsleep()

vled=LED
alarm = Pin(vled, Pin.OUT)

alarm.value(0)

#connetti wifi Station
do_connect()

#indirizzo server a cui mandare i dati
vserver=SERVER
#while True:
#    time.sleep_ms(750)
#    time.sleep_ms(750)
dati=leggi_sensore()
jdati=ujson.loads(dati)
print(dati)
req = post(vserver + "/dati.php",data=None,json=jdati)
print(req.text)
print("deepsleep tra 1,5 seocndi")
time.sleep_ms(750)
time.sleep_ms(750)

deep_sleep(30000)