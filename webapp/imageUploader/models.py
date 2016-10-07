from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Image model with all required field. Similar table present in sqllite3
class imageModel(models.Model):
    caption = models.CharField(max_length=100, blank = True)
    modelPic = models.ImageField(upload_to='ImageFolder/')
    uploadTime = models.DateTimeField(default = datetime.now)
    user = models.ForeignKey(User, default=1)
    class Meta:
        ordering = ['-uploadTime']
# Ordering would make sure that data is always returned in descending sorted order of uploadTime

