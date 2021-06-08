from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *

def CreateCustomer(sender,instance,created, **kwargs):
	if created:
		Customer.objects.create(
            user=instance,
            name = instance.username,
            email = instance.email,
            profile_pic = "placeholder.png",

        )
		
post_save.connect(CreateCustomer,sender=User)




