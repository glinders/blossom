
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
>>> user.pk  # primary key
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

