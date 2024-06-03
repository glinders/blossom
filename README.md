
### migrations
to see actual SQL code when the migration is executed, run:

`python manage.py sqlmigrate ccf 0001`

where `ccf` is the app-name and `0001` is the number in the migration
filename, e.g. `0001_initial.py`

### access models in database using django shell
```
(venv311_django) PS C:\projects\django\blossom> python manage.py shell    
Python 3.11.5 on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from django.contrib.auth.models import User           
>>> from ccf.models import Post  
>>> User.objects.all()
<QuerySet [<User: admin>, <User: brenda>, <User: user0>, <User: user1>]>
>>> User.objects.all().first()
<User: admin>
>>> User.objects.filter(username='brenda')
<QuerySet [<User: brenda>]>
>>> User.objects.filter(username='brenda').first()
<User: brenda>
>>> user = User.objects.filter(username='brenda').first()
>>> user
<User: brenda>
>>> user.id
2
>>> user.pk  # primary key[migrations](ccf%2Fmigrations)
2
>>> user = User.objects.get(id=3)
>>> user
<User: user0>
>>> post_1 = Post(title='post 1', content='content for post 1', author = user)
>>> post_1.save()
>>> Post.objects.all()
<QuerySet [<Post: post 1>]>
>>> 
```
show posts from user and add post:
```
>>> user = User.objects.filter(username='brenda').first()
>>> user.post_set.all()
<QuerySet [<Post: post 2>]>
>>> user.post_set.create(title='post 3', content='content post 3')
<Post: post 3>
>>> user.post_set.all()                                            
<QuerySet [<Post: post 2>, <Post: post 3>]>
```

### add posts (test) data using shell
```
(venv311_django) PS C:\projects\django\blossom> python manage.py shell    
Python 3.11.5 on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import json
>>> from ccf.models import Post  
>>> with open('test_posts.json') as f:
...     posts_json = json.load(f)
... 
>>> with open('test_posts.json') as f:
...     posts_json = json.load(f)
... 
>>> for post in posts_json:
...     post = Post(title=post['title'], content=post['content'], author_id=post['user_id'])
...     post.save()
... 
>>> exit()
(venv311_django) PS C:\projects\django\blossom> 
```

### github  gnutls_handshake() failed: Error in the pull function.

See https://github.com/microsoft/WSL/issues/5346#issuecomment-1016469312

gist:
```
The problem was in a mismatch between VPN MTU and Linux under WSL2 MTU sizes.

It can be identified via 2 commands:

Windows PowerShell (run as administrator)

netsh interface ipv4 show subinterfaces

Notice the first row - it shows how big MTU is allowed in your VPN.

Linux (inside WSL2) console

ip addr

Notice the row starting 'eth0' - its MTU must match or be lower that the one above.

In my case the MTU in Linux was higher.

Solution

The following command instantly solves the problem:

sudo ip link set dev eth0 mtu 1400 (update MTU value to fit your VPN)

```