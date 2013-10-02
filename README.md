loggins
-------

a very simple django app that tracks logins and logouts from public
computers in our library.  it collects data recording a machine name,
its status, and a timestamp.  its API is exposed by tastypie.


installation
------------

these instructions are optimized for running on a newly installed
Ubuntu 12.04 LTS host.

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

Install Git
```
$ sudo apt-get install git-core
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

get the code for this application, loggins, from github, then check
out the tag to deploy:

```
$ git clone https://github.com/gwu-libraries/loggins.git
$ cd loggins
$ git checkout tag_foo
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
then add in correct ADMINS, DATABASE and SNMP_COMMUNITY_STRING info.
Add host info in ALLOWED_HOSTS.
Note: If you don't have a SNMP community string, just enter 'public'
```
$ cd loggins
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

set up the db with django. WARNING: Be sure you are still using your virtualenv. DO NOT create a superuser when prompted!
```
$ ./manage.py syncdb
```

Migrate the database to the latest updates
```
$ ./manage.py migrate
```

Create the database super user
```
$ ./manage.py createsuperuser
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
apache's sites, then edit it to use proper paths and hostname info,
optionally enabling SSL (cert/key handling follows standard approach
see http://httpd.apache.org/docs/2.2/ssl/ for details):
```
$ sudo cp loggins/apache.conf.template /etc/apache2/sites-available/loggins_beta_001
[EDIT EDIT EDIT]
```

[optionally disable the default site, then] enable the loggins site, 
then reload apache:
```
$ sudo a2dissite default
$ sudo a2ensite loggins
$ sudo /etc/init.d/apache2 reload
```

you should be up and running. to test it out, use curl:
```
curl script to record a login event
$ curl -i -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: ApiKey <YOURUSERNAME>:<YOURAPIKEY>" -X PUT -d "{\"ip_address\":\"<IPADDRESS>\",\"state\":\"i\",\"observation_time\":\"$(date +%Y-%m-%dT%H:%M:%S)\"}" http://<YOUR.SERVER.NAME>:<PORT>/api/v1/location/<HOSTNAME>/
```
```
curl script to record a logout event
$ curl -i -H "Content-Type: application/json" -H "Accept: application/json" -H "Authorization: ApiKey <YOURUSERNAME>:<YOURAPIKEY>" -X PUT -d "{\"ip_address\":\"<IPADDRESS>\",\"state\":\"a\",\"observation_time\":\"$(date +%Y-%m-%dT%H:%M:%S)\"}" http://<YOUR.SERVER.NAME>:<PORT>/api/v1/location/<HOSTNAME>/
```

Additional Location attributes that can be updated using the API are,
```"building", "floor", "hostname", "os", and "station_name"```
to create user/accounts/api keys, go to the django admin site at 
```/admin```, and under ```Users``` create new users as needed. new
api keys are generated when you create new accounts.  the generated
api key for each user is listed at the bottom of their account page
in the admin ui.

to update existing api keys, go to the django admin page for the user
account in question and update the api key value at the bottom.

to generate some test data, use the ```login_monkey``` management
command.  this will generate new records, one per random host, along
with a set of initial testing hosts, at an interval you can specify.
by default, it creates 20 "monkey" hosts, spread throughout the first
floors of three of our libraries ('g', 'e', and 'v').  for example,
this will add a new record every five seconds:

```
$ ./manage.py login_monkey --interval 5 --verbose
```
