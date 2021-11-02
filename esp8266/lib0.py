from constants import PIN_1WIRE, PSW, SID
import usocket
import time
import machine
import onewire, ds18x20
from config import bus, pin



def leggi_sensore():
    # imposta il bus onewire sul pin PIN_1WIRE
    #pin=PIN_1WIRE  #messo in config
    #pinOnewire = machine.Pin(pin)

    # crea il bus sul pin pinOnewire
    #bus = ds18x20.DS18X20(onewire.OneWire(pinOnewire)) #messo in config

    # cerca dispositivi sul bus 
    roms = bus.scan()
    if roms:      
        print('Dispositivi trovati al pin: ' + str(pin), roms)

    #        print('temperatures:', end=' ')
        bus.convert_temp()
        time.sleep_ms(750)
        vterra=bus.read_temp(roms[0])
        vmezza=bus.read_temp(roms[1])
        valto=0.0

        print()
        dati='{"terra": ' + str(vterra) + '  ,   "mezza":  ' + str(vmezza) + '  ,  "alto": ' + str(valto) + '}'
        return dati

# funzioni per connessione wifi
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
#        vSID=input("Inserire SID:")
#        vPSW=input("Inserire password:")
        vSID=SID
        vPSW=PSW        
        print('connecting to network...')
        wlan.connect(vSID, vPSW)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    
#funzioni http
class Response:

    def __init__(self, f):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)


def request(method, url, data=None, json=None, headers={}, stream=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json is not None:
#            assert data is None
            import ujson
            data = ujson.dumps(json)
            s.write(b"Content-Type: application/json\r\n")
        if data:
            s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"\r\n")
        if data:
            s.write(data)

        l = s.readline()
        #print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            #print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and 300 < status < 400:
                new_url = (l[10:-2]).decode('utf8')
                return request(method, new_url, data, json, headers, stream)
    except OSError:
        s.close()
        raise

    resp = Response(s)
    resp.status_code = status
    resp.reason = reason
    return resp


def head(url, **kw):
    return request("HEAD", url, **kw)

def get(url, **kw):
    return request("GET", url, **kw)

def post(url, **kw):
    return request("POST", url, **kw)

def put(url, **kw):
    return request("PUT", url, **kw)

def patch(url, **kw):
    return request("PATCH", url, **kw)

def delete(url, **kw):
    return request("DELETE", url, **kw)