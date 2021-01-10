
import json,os,sys

from chalice import Chalice
from chalicelib.ssh import (ssh_run,decrypt_key,get_pubkey,get_hostkey)

app = Chalice(app_name='lambda-homecontrol')

pw = os.environ['PASSWD'].encode()
salt = b'lljFQLs9ikpR_Ke8-OA0CQ=='
enc_key = b'gAAAAABf-0hmxefip7yz6ye3KClswpOxUGyZye4m6h7qL_kKqcYePkDO7MoxCI0aSIPLNtKUd9_uhFGBGy7f6D5ou3O7_dc5R2uZyzCRNPhGR9RZhCUWPgVuI9CpSsD_nW_tOH54aF5m6HI9180SEQqfCIl3c89yIiesYUj-ijIBJj8ocd9oKCG77llWheyYJX39ntBZaYhS-JDWwdmyU5oDtVJWDAd2PQ4qcoqbV6xTUwadJ8Q5uaYs61yGqtoj7KQldFAXXNwzpAdSQMx4vgWbarykQjyVgrSPv5p6ZEu8bYEVXDgxQTXBdjKc1X43FQ1Ief7CNiVP6Cadio75w9MuucS45QQ-dZs15j2omv0COb3k9XnHXL6xfRODBN4QPCcflnPZajaDLNUJrhlqL84zInrF472yXi5K63f4em0mZJu_5lOsd38zlY-buQMEyiSwLh96PHJXkQvmyfSQjps1Y1-vv-ScAd2nLkYdD2y31E0nk5pW52PNI26QOtuojgsHaRCmSy9UsB2wLkIyeXN958EQiLj73ZaUtSuoQtVuVOwmPNrvqmILP4g4ce4cjU2iFMdMTuqgyES9q4eLLfeEa5SuIHADLg=='

known_hosts = '* ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBNu45p24jDSYpDJa11FLNX7dHyNb70AJzqCKcDcm22wTQpkgVHxJO32dKAa/guLwgZXXoozCLsBVkxzf6NLNR6M='

user = 'lambda'
host = 'home.pchak.net'
port = 37571
private_key = decrypt_key(pw,salt,enc_key)
host_key = get_hostkey(known_hosts)

@app.route('/')
def index():
    return {'status': 'ok'}

@app.route('/status/{device}')
def status(device):
    try:
        return json.loads(ssh_run(host,port,user,private_key,host_key,f'{device} status'))
    except ValueError as e:
        return {'error': str(e)}

@app.route('/on/{device}')
def on(device):
    try:
        return json.loads(ssh_run(host,port,user,private_key,host_key,f'{device} power on'))
    except ValueError as e:
        return {'error': str(e)}

@app.route('/off/{device}')
def off(device):
    try:
        return json.loads(ssh_run(host,port,user,private_key,host_key,f'{device} power off'))
    except ValueError as e:
        return {'error': str(e)}

@app.route('/toggle/{device}')
def toggle(device):
    try:
        return json.loads(ssh_run(host,port,user,private_key,host_key,f'{device} power toggle'))
    except ValueError as e:
        return {'error': str(e)}

@app.route('/pubkey')
def pubkey():
    return {'pub_key': get_pubkey(private_key)}

