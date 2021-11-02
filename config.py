from constants import PIN_1WIRE
from machine import Pin
import gc
import onewire, ds18x20

gc.collect()


pin=PIN_1WIRE
pinOnewire = Pin(pin)
bus = ds18x20.DS18X20(onewire.OneWire(pinOnewire))