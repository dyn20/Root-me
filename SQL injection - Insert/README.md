# SQL injection - Insert (medium - 40pts)

Ở challenge này gồm có hai phần chính là: register để đăng kí tài khoản mới và login để đăng nhập vào tài khoản. 

Vì challenge này thuộc dạng sql injection – insert nên chúng ta sẽ tập trung vào khai thác ở phần register.

Sau khi đăng kí một tài khoản mới thì khi đăng nhập lại thông tin email và username của user sẽ được in ra:

![image](https://user-images.githubusercontent.com/83667873/160068407-602266b9-0ce1-4eb3-ae18-74a873ea86c7.png)

![image](https://user-images.githubusercontent.com/83667873/160068424-b2622ce5-54ac-4850-a6fb-826cf798d732.png)

Khi chúng ta inject dấu ' vào parameter username và password thì sẽ nhận được phản hồi là “char not authorised” chỉ có khi inject vào email thì nó mới hoạt động, vậy nên trong bài này parameter để chúng ta thực hiện khai thác sqli là email.

Tóm lại ý tưởng của bài này như sau:

Thực hiện lồng query vào như thế nào đó để thông tin chúng ta cần tìm được sử dụng để làm thông tin đăng kí cho email, sau khi đăng kí tài khoản thành công và thực hiện đăng nhập lại thì sẽ lấy được thông tin thông qua thông tin email.

Trong bài này chúng ta không thể thực hiện nối chuỗi theo cách thông thưởng bởi vì theo như mình test thì dbs đang được sử dụng không thể sử dụng cách nối chuỗi 'ab'||'cd' -> 'abcd', bên cạnh đó không thể inject vào para username và password nên việc sử dụng function concat là no hope.

Nhưng chúng ta có thể thực hiện khai thác được thông tin theo cách khác. Ví dụ kí tự lấy được là ‘a’, chúng ta thực hiện đổi kí tự a sang dạng số, sau đó thực hiện cộng.

Ví dụ:

![image](https://user-images.githubusercontent.com/83667873/160068665-1e96c6cc-0e3a-4d40-9b42-6809b57aacab.png)

Sau khi có kết quả chúng ta chỉ cần convert ngược lại thành dạng string là được.

Nhưng, trong bài này vẫn còn một số khó khắn nữa:

-	substr bị filter -> chúng ta không thể lấy từng kí tự
-	hex() không thể dung để lấy nguyên chuỗi dù nó không bị cấm. Nguyên nhân:

![image](https://user-images.githubusercontent.com/83667873/160068746-3881a653-f3a4-4e8f-9797-5fd129d1ebfe.png)

Khi flag của chúng ta là một chuỗi ngắn, khi convert thành hex vẫn là một số có thể chấp nhận được thì query sẽ thành công:

![image](https://user-images.githubusercontent.com/83667873/160068781-25fb5a90-41d2-4165-94be-6e0524e491ed.png)


Nhưng trường hợp là một chuỗi dài, vượt quá giới hạn:

![image](https://user-images.githubusercontent.com/83667873/160068813-60809614-e025-433c-bf88-af1b67646ff3.png)

Thật không may là của chúng ta rơi vào trường hợp thứ 2. Nên kết quả sẽ là:

![image](https://user-images.githubusercontent.com/83667873/160068848-0b1c657e-9e0b-448e-8cb7-428b0cecaf91.png)

Chúng ta phải tìm một solution khác:

![image](https://user-images.githubusercontent.com/83667873/160068880-d10d8090-fdc9-4e3a-991f-87fbc298efd0.png)

Ở đây chúng ta có thể thấy function ASCII(): trả về numeric value của kí tự ngoài cùng bên trái. Ví dụ:

![image](https://user-images.githubusercontent.com/83667873/160068931-ad3c069c-52d7-4f5b-abfa-7f65cdf4020e.png)

Kết quả trả về 97 là numeric value của ‘a’.

Oke, nhưng chỉ lấy được một kí tự, còn những kí tự sau thì như thế nào?

Lướt xuống tí, chúng ta sẽ thấy function replace(), với những kí tự đã tìm được mình sẽ thực hiện replace với ‘’ để lấy được kí tự tiếp theo:

![image](https://user-images.githubusercontent.com/83667873/160068976-4e40c59b-38da-4f53-bb9e-fdd1db9b75ea.png)

Ví dụ lấy kí tự c trong chuỗi 'abcd':

![image](https://user-images.githubusercontent.com/83667873/160069699-dfce421b-a70d-420c-85dd-3746bdddcf34.png)

-> Kết quả trả về numeric value của 'c'

Link: https://dev.mysql.com/doc/refman/8.0/en/string-functions.html

Theo cách này chúng ta sẽ dần table và column chứa flag, vì mình đã làm bài này khá lâu về trước nên mình lười làm chi tiết lại quá (table: flag, column flag).

Solve code:

![image](https://user-images.githubusercontent.com/83667873/160069209-85fc3d42-f5c3-4bd2-96e4-612423ff4d9b.png)



