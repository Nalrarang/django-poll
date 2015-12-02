from django.db import models
from django.utils import timezone

# Create your models here.
class Poll(models.Model):
    phonenumber = models.CharField(max_length=11)
    survey = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)

    def user_poll(self):
        self.save()



