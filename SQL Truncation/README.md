# SQL Truncation (Medium - 35 pts)

In this challenge, there are register form to register new account and a validation form where we can enter admin's password to access admin panel.

- /register.php:

![image](https://user-images.githubusercontent.com/83667873/151130000-6da9bf5c-84e0-42be-a2e7-aca1639c0b7f.png)

- /admin.php:

![image](https://user-images.githubusercontent.com/83667873/151130045-5b779f81-b9b9-4217-ae05-42be13c90b76.png)

## Something about SQL Truncation:

SQL Truncation is a flaw in database configuration in which an input is truncated (deleted) when added to the database due to surpassing the maximum defined length (For example: if table user has column username wih defined length is 20,
if you create a new user with username length out of 20, characters from 21th character will be truncated.

You can use SQL Truncation to create a new user with have the same username with existed username (admin or somthing else)

For example:

In databse has admin user which has username is admin. And the defined length of username is 20

I will create new user with username:

```
admin+++++++++++++++hihi (+ is whitespace)
```

Because, the defined length of username is 20, so character from 21th character will be truncated.

So the username of new user in database now will become:

```
admin+++++++++++++++
```
Next time an attacker logs in to the application with the admin account, the database will search for all matching accounts and will consider them valid for logging in. Therefore any entry with username as admin with space or without is a valid entry that can be used to authenticate to the application.

*Reference:https://medium.com/r3d-buck3t/bypass-authentication-with-sql-truncation-attack-25a0c33ab87f*

Back to challenge, let see table user:

![image](https://user-images.githubusercontent.com/83667873/151136550-14fef859-9646-45e0-8969-eeb28f62093f.png)

You can see that login or user has defined length is 12, so we just neet to create an account has more 12 character (12 character 'admin' and whitespace plus random characters after).

![image](https://user-images.githubusercontent.com/83667873/151137032-5b747275-4cfa-402a-a4ed-1002cb419d9c.png)

Account create successfully:

![image](https://user-images.githubusercontent.com/83667873/151137089-8d803918-0eef-4914-8d34-f51cc0e33279.png)

Use password of the account you just created to validate, you can access to admin panel and get flag:

![image](https://user-images.githubusercontent.com/83667873/151137385-4dd686d1-c79a-4c0d-b855-32ca675058e8.png)


