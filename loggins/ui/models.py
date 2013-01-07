from django.db import models

class Record(models.Model):

    LOGIN = 'i'
    LOGOUT = 'o'
    EVENT_TYPES = [
        (LOGIN, 'login'),
        (LOGOUT, 'logout'),
        ]

    host = models.CharField(max_length=50, db_index=True)
    event = models.CharField(db_index=True, max_length=2,
            choices=EVENT_TYPES, default=LOGIN)
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True) 
