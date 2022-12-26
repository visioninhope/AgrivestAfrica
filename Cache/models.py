from django.db import models
from Log.models import User

class Password_Token(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  token = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.user.username
  