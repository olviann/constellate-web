from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=25)
    birth_date = models.CharField(max_length=20)
    birth_time = models.CharField(max_length=20)
    birth_place = models.CharField(max_length=255)
    rising = models.CharField(max_length=15)
    sun = models.CharField(max_length=15)
    moon = models.CharField(max_length=15)
    mercury = models.CharField(max_length=15)
    venus = models.CharField(max_length=15)
    mars = models.CharField(max_length=15)
    jupiter = models.CharField(max_length=15)
    saturn = models.CharField(max_length=15)
    sun_rec = models.TextField(max_length=500)
    moon_rec = models.TextField(max_length=500)
    true_node_rec = models.TextField(max_length=500)
    svg_content = models.TextField()