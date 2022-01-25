# SQL Injection - Filter bypass (Hard - 80 pts)

After reviewing the entire website, I found that `id` parameter to show user's information is where we can inject SQL injection.

```
http://challenge01.root-me.org/web-serveur/ch30/?action=membres&id=
```
![image](https://user-images.githubusercontent.com/83667873/151038833-ebcc404a-9e4b-416f-b827-6bc1159b5a6c.png)

***Tip:***

*Why I know that. If you get used to SQL injection, you will be sensitive with where the information are leak.*

But in this challenge, there are a lot of characters and words are filtered. I will list some I met: `or, and, ||, /**/, union, select, join, white space, %0a, %0b, %0c, ',comma(,),...`

But with `select` and `union`, just upercase is filtered, when I change these words to lowercase, we can bypass.

With these information, my idea is use  `UNION` and `SELECT` to leak information from table membres. Table name and columns name is provide, you can view source to see:

![image](https://user-images.githubusercontent.com/83667873/151036192-d74d4ba7-d7f2-48cf-8a7b-cd4383bfbcd7.png)

If don't have above provided information, this challenge will become very difficult because when I test, `information_schema.tables` if filtered so we can't leak table name as well as columns name easily.

Okay, back to challenge, because whitespace and many tab character is filter so I will use %09 to replace for whitespace.

Now, our payload will look like:

```
id=9%09UNION%09SELECT%09pass,1,1,1%09FROM%09membres%09LIMIT%091
```
But the comma (,) character is filtered, so we can use it to select like below payload.

So we must find a way to change this select query to other query which have the same meaning.

After searching, I found solution:

For example, my query is:
```
select 1,2,3;
```
![image](https://user-images.githubusercontent.com/83667873/151038392-2493818d-620f-4fe1-b817-338238991cca.png)

I will rewrite below query use `join`:

```
select * from ((select 1)A join (select 2)B join (select 3)C);
```
![image](https://user-images.githubusercontent.com/83667873/151038432-c4351dfc-8898-4457-bcdf-33d97eaf2400.png)

But there is a small note that with `join` word, the upercase is filtered, but lowercase is not, so in your payload, you must to use `JOIN`.

Final payload:

```
id=9%09UNION%09SELECT%09*%09FROM%09((SELECT%09pass%09FROM%09membres%09LIMIT%091)A%09JOIN%09(SELECT%092)B%09JOIN%09(SELECT%093)C%09JOIN%09(SELECT%093)D)
```
