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

