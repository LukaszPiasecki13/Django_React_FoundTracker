from django.db import models
from django.contrib.auth.models import AbstractUser



class UserProfile(AbstractUser):

    STATUS = (
        ('regular', 'regular'),
        ('admin', 'admin')
    )

    CURRENCIES = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('PLN', 'PLN')
    )
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=30, choices=STATUS, default='regular')
    main_currency = models.CharField(max_length=3, choices=CURRENCIES, default='PLN')


    def __str__(self):
        return self.username
