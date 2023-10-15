from django.db import models
from django.utils import timezone

class Inbox(models.Model):
    title = models.CharField(max_length=300)
    image = models.ImageField(default='default.jpg', upload_to='message_tags')
    content = models.CharField(max_length=3000)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=300, default='AgrivestAfrica')

    def __str__(self):
        return self.title
  

class Team(models.Model):
    name = models.CharField(max_length=300)
    position = models.CharField(max_length=300)
    bio = models.TextField(max_length=3000)
    image = models.ImageField(default='image.jpg', upload_to='team_pics')
    def __str__(self):
        return self.name

class Board(models.Model):
    name = models.CharField(max_length=300)
    position = models.CharField(max_length=300)
    bio = models.TextField(max_length=3000)
    image = models.ImageField(default='image.jpg', upload_to='team_pics')
    def __str__(self):
        return self.name
    
class Advisor(models.Model):
    name = models.CharField(max_length=300)
    position = models.CharField(max_length=300)
    bio = models.TextField(max_length=3000)
    image = models.ImageField(default='image.jpg', upload_to='team_pics')
    def __str__(self):
        return self.name