from django.db import models


# Create your models here.
class ImageData(models.Model):
    image = models.ImageField(upload_to='img')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    upload_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        app_label = 'isbs'
        db_table = 'image_data'