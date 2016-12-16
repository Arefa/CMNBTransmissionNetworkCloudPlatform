from django.db import models


class NetworkElement(models.Model):
    ne_name = models.CharField(max_length=100)
    ne_type = models.CharField(max_length=100)
    ring_name = models.CharField(max_length=100)
