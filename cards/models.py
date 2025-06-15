from django.db import models

class Card(models.Model):
    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.word
