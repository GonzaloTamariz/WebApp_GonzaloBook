from uuid import uuid4
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
# Create your models here.

User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    firstName = models.CharField(max_length= 100, blank=True)
    lastName = models.CharField(max_length= 100, blank=True)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to = 'profile_images' , default= 'blank-profile-picture.png')
    location = models.CharField(max_length= 100, blank=True)
    workingat = models.CharField(max_length= 100, blank=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key= True, default= uuid4) #This is the primary key
    user = models.CharField(max_length= 100)
    image = models.ImageField(upload_to = 'post_images')
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(default= datetime.now)
    num_of_likes = models.TextField(default=0)

    def __str__(self):
        return self.user
    
class LikePost(models.Model):
    post_id = models.CharField(max_length= 500)
    username = models.CharField(max_length= 100)
    
    def __str__(self):
        return self.user