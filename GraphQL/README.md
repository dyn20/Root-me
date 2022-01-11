# GraphQL - Medium

Trước tiên, chúng ta tạo account và thực hiện đăng nhập.

Thông thường để kiểm tra xem một trang web có khả năng bị khai thác GraphQL injection hay không, thì chúng ta sẽ kiểm tra xem có tồn tại đường dẫn:
- /graphql
- /grpahiql
- /graphql.php
- /graphql.console

Tham khảo: https://book.hacktricks.xyz/pentesting/pentesting-web/graphql

Sử dụng burpsuite, chúng ta kiểm tra trong HTTP history sẽ thấy một request tới /graphql dưới method là POST:

![image](https://user-images.githubusercontent.com/83667873/148902408-626c86fb-92de-4e1c-9403-169549de0fab.png)

![image](https://user-images.githubusercontent.com/83667873/148902488-88371321-54c9-479c-8bd2-d01c1cfd6099.png)

Trong hình có câu query để list ra id, slug, name, createAt của những bài post user có thể xem.

Mình sẽ chỉnh một tí ở câu query cho dễ nhìn:

![image](https://user-images.githubusercontent.com/83667873/148902800-7f6fa170-d48c-4d08-8986-00b6124bbe19.png)

Thử liệt kê tên của tất cả các types đang được sử dụng:

```
query={__schema{types{name,fields{name}}}}
```
![image](https://user-images.githubusercontent.com/83667873/148903388-71480b20-4f86-46b8-8b62-1806f0111b91.png)

Ở đây chúng ta thấy có 4 types chính là user, post, nude, comment.

Hiển thị chi tiết toàn bộ field và args cho từng field. Hiểu nôm na nó như việc chúng ta đang đi leak thông tin của các table tên bảng, tên cột trong SQL :
```

query IntrospectionQuery {__schema {queryType { name }mutationType { name }subscriptionType { name }types {...FullType}directives {\n        name\n        description\n        args {\n          ...InputValue\n        }}}}\n\n  fragment FullType on __Type {\n    kind\n    name\n    description\n    fields(includeDeprecated: true) {\n      name\n      description\n      args {\n        ...InputValue\n      }\n      type {\n        ...TypeRef\n      }\n      isDeprecated\n      deprecationReason\n    }\n    inputFields {\n      ...InputValue\n    }\n    interfaces {\n      ...TypeRef\n    }\n    enumValues(includeDeprecated: true) {\n      name\n      description\n      isDeprecated\n      deprecationReason\n    }\n    possibleTypes {\n      ...TypeRef\n    }\n  }\n\n  fragment InputValue on __InputValue {\n    name\n    description\n    type { ...TypeRef }\n    defaultValue\n  }\n\n  fragment TypeRef on __Type {\n    kind\n    name\n    ofType {\n      kind\n      name\n      ofType {\n        kind\n        name\n        ofType {\n          kind\n          name\n        }\n      }\n    }\n  }

```
Tham khảo: https://gist.github.com/craigbeck/b90915d49fda19d5b2b17ead14dcd6da

Chúng ta thấy ở trong nude code flag, khả năng cao là secret mà chúng ta cần tìm đang nằm ở đây:

![image](https://user-images.githubusercontent.com/83667873/148906505-26e13c7d-6053-4a3e-ac23-807ac6c29414.png)

Mình thử query vào nude xem sao nhưng không có quyền access:

![image](https://user-images.githubusercontent.com/83667873/148906759-242399c7-ae48-4775-befe-e0b9e465479f.png)

Quan sát trong Comment chúng ta sẽ thấy có mutation createComment cho phép chúng ta tạo mới một comment.

Có một điều đáng lưu ý ở đây là ở trong args của comment chúng ta thấy có nude. Vậy nên chúng ta có thể tạo mới một comment, sau đó query tới nude trong comment và lấy flag mà không cần phải query trực tiếp vào nude:

Tạo mới một comment cần có: userId, postId, nudeId, comment (nội dung comment):

![image](https://user-images.githubusercontent.com/83667873/148908386-16c93e8d-e234-43fe-a20e-9a2836e8b591.png)

Xác định userId của mình:

![image](https://user-images.githubusercontent.com/83667873/148908660-557c0f56-4005-4653-bf76-a1f49b31f34e.png)

PostId:

Ở đây có 3 post chúng ta có thể chọn một trong 3 post để tạo comment vào

![image](https://user-images.githubusercontent.com/83667873/148908731-dba7ea96-7b98-4316-b810-7f104161861f.png)

Nude vì mình không biết flag đang nằm ở nudeId bao nhiêu nên mình sẽ để là 1:

```
mutation { createComment(userId:1,postId:1,nudeId:1,comment:\"hehe\"){comment,id}}
```
![image](https://user-images.githubusercontent.com/83667873/148909671-b82f42da-c563-40c3-a483-fa10585427bd.png)

Bây giờ mình thử đi đọc comment vừa tạo, nhưng có một vấn đề là comment chỉ được đọc bởi admin, nên mình không thể đọc trực tiếp được:

![image](https://user-images.githubusercontent.com/83667873/148909878-d2bf5827-df88-4c5b-995a-b8be8280e026.png)

Kiểm tra lại trong field post chúng ta sẽ thấy có comments, chứa tất cả comment của bài post. Vậy nên chúng ta sẽ đọc comment thông qua bài post.

Lúc nãy mình thực hiện comment vào bài post có id là 1 nên giờ mình sẽ đọc commnent từ bài post này ra:

![image](https://user-images.githubusercontent.com/83667873/148910836-729ef026-a394-4501-b489-8554ae9aad7e.png)

Thành công đọc được comment và flag ở trong nude, nhưng thứ chúng ta cần tìm vẫn chưa có ở đây. Chứng tỏ flag không nằm trong nude có nudeId là 1. 

Giờ mình sẽ thêm lại comment mới nhưng lúc này nudeId là 2:

![image](https://user-images.githubusercontent.com/83667873/148911077-2feb8a66-48da-46bd-a980-6db98dcbdfa4.png)

Đến đây thì chúng ta sẽ có được flag cần tìm:

![image](https://user-images.githubusercontent.com/83667873/148911485-1efd6099-be80-40d1-b5ea-1fb9d4eddd0a.png)



