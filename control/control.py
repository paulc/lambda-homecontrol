#!/usr/bin/env python3

import configparser,json,sys
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import URLError

def tasmota(host,command):
    return json.load(urlopen(f'http://{host}/cm',data=urlencode(dict(cmnd=command)).encode()))

if __name__ == '__main__':
    devices = configparser.ConfigParser()
    devices.read('devices.ini')
    response = []
    error = []
    for l in sys.stdin:
        try:
            target,command = l.strip().split(maxsplit=1)
            device = devices[target]
            device_func = locals()[device['func']]
            device_host = device['host']
            result = device_func(device_host,command)
            response.append(dict(device=device_host,command=command,result=result))
        except Exception as e:
            error.append(dict(input=l.rstrip(),error=str(e)))
    json.dump(dict(response=response,error=error),sys.stdout)
