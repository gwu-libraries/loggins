loggins
-------

a very simple django app that tracks logins and logouts from public
computers in our library.  it receives PUTs recording a machine name,
whether the event is a login or logout, and a timestamp.  its API
is exposed by tastypie.


installation
------------

these instructions are optimized for running on a newly installed
Ubuntu 10.04 LTS host.

```
$ sudo apt-get install python-dev python-virtualenv libapache2-mod-wsgi
```

same for whichever db you want to use:
```
$ sudo apt-get install postgresql-9.1 postgresql-server-dev-9.1
[or]
$ sudo apt-get install mysql-server libmysqld-dev
[etc]
```

create the database you'll use (pgsql example included, do equiv
for mysql):
```
% sudo su - postgres
(postgres)% psql
postgres=# create user MYUSERNAME with createdb password 'MYPASS';
CREATE ROLE
postgres=# \q
(postgres)% exit
% createdb -U MYUSERNAME MYDBNAME -W
Password: <'MYPASS'>
```

set up a directory to host the deployed code, and a deployment name
inside there (setting perms as needed):

```
$ mkdir -p /loggins/tag_foo
$ cd /loggins/tag_foo
```

create and activate a virtualenv:

```
$ virtualenv --no-site-packages ENV
$ source ENV/bin/activate
```

install dependencies (note: based on db server choice, use psycopg2
or MySQL-python as appropriate):

```
$ pip install -r requirements.txt
```

copy over the local settings template to a real local settings file,
then add in correct ADMINS and DATABASE info.
```
$ cd /loggins/tag_foo/loggins
$ cp loggins/local_settings.py.template loggins/local_settings.py
[edit edit edit]
```

copy over the wsgi template to a real wsgi file, uncomment the
virtualenv details and specify the path to your virtualenv:
```
$ cp loggins/wsgi.py.template loggins/wsgi.py
[edit edit edit]
```

pull in the static files (for admin, etc.):
```
$ ./manage.py collectstatic
```

set up the db with django:
```
$ ./manage.py syncdb
[add a superuser, you'll need it]
```

at this point you should be able to run the app in debugging mode:
```
$ ./manage.py runserver
```

if your high ports are closed and you need to look at it locally
at the commandline, use links:
```
$ links http://127.0.0.1:8000/
```

if it's working, you're good to go!

to install into apache, copy and install your apache config into 
apache's sites, then edit it to use proper paths and hostname info:
```
$ sudo cp loggins/apache.conf.template /etc/apache2/sites-available/loggins_beta_001
[EDIT EDIT EDIT]
```

[optionally disable the default site, then] enable the site, then reload 
apache:
```
$ sudo a2dissite default
$ sudo a2ensite loggins
$ sudo /etc/init.d/apache reload
```

you should be up and running. to test it out, use curl:
```
$ curl -i -H "Content-Type: application/json" -H "Accept: application/json" -u YOURUSERNAME:YOURPASSWORD  -X POST -d '{"event":"i","hostname":"test1"}' http://YOUR.SERVER.NAME:PORT/api/1/record/
```
