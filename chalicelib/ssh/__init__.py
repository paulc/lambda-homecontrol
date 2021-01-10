
import asyncio,base64,getpass,io,os,sys
import asyncssh

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def generate_encrypted_key(pw,alg='ssh-ed25519'):
    pk   = asyncssh.generate_private_key(alg)
    salt = os.urandom(16)
    kdf  = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000)
    key  = base64.urlsafe_b64encode(kdf.derive(pw))
    enc_key = Fernet(key).encrypt(pk.export_private_key())
    return (base64.urlsafe_b64encode(salt),enc_key,pk.export_public_key())

def decrypt_key(pw,salt,enc_key):
    kdf  = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=base64.urlsafe_b64decode(salt),iterations=100000)
    key  = base64.urlsafe_b64encode(kdf.derive(pw))
    return asyncssh.import_private_key(Fernet(key).decrypt(enc_key))

def get_pubkey(key):
    return key.export_public_key().rstrip().decode()

def get_hostkey(host_key):
    return asyncssh.import_known_hosts(host_key)

def ssh_run(host,port,user,private_key,host_key,stdin):
    async def _run():
        async with asyncssh.connect(host,
                        port=port,
                        client_keys=[private_key],
                        known_hosts=host_key,
                        username=user) as conn:
            result = await conn.run(check=True,stdin=io.BytesIO(stdin.encode()))
            return result.stdout.rstrip()
    try:
        f = _run()
        return asyncio.get_event_loop().run_until_complete(f)
    except (OSError, asyncssh.Error) as exc:
        raise ValueError('SSH connection failed: ' + str(exc))

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '--decrypt':
        pw = getpass.getpass().encode()
        salt = input("Salt: ").encode()
        enc_key = input("Encrypted Key: ").encode()
        pk = decrypt_key(pw,salt,enc_key)
        print("\n# PRIVATE KEY")
        print(pk.export_private_key().decode())
        print("\n# PUBLIC KEY")
        print(pk.export_public_key().decode())
    else:
        pw = getpass.getpass().encode()
        salt,enc_key,pub_key = generate_encrypted_key(pw)
        print(f'salt = {salt}\nenc_key = {enc_key}\npub_key = {pub_key}')

