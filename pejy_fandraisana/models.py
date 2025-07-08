from django.db import models

# Create your models here.
class Sokajy(models.Model):
    anarana = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.anarana

class Ohabolana(models.Model):
    ohabolana = models.TextField()
    mpanoratra = models.CharField(max_length=100, blank=True)
    sokajy = models.ForeignKey(Sokajy, on_delete=models.CASCADE)

    def __str__(self):
        return self.mpanoratra