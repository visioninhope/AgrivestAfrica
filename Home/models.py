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
  