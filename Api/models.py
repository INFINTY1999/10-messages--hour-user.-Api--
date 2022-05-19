from django.db import models
from django.contrib.auth.models import User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class message(models.Model):
    id = models.AutoField(unique=True,primary_key=True,editable=False)
    message = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
    
    def __str__(self) :
        return str(self.id)
    
    def message_10(a):
        return message.objects.filter(created_by = a).order_by('-updated_at').all()[9:10]
    
    class Meta :
        ordering = ['-updated_at']
