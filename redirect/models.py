from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userdisplay = models.CharField(max_length=150, null=True)
    
@receiver(models.signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        
@receiver(models.signals.post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile') == False:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()

class Couplet(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    in_url = models.CharField(max_length=2048, null=True, unique=True)
    out_url = models.CharField(max_length=2048, default='')
