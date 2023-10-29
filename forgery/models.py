from django.db import models

# Create your models here.
class Images(models.Model):
    uploaded_image = models.ImageField(upload_to='upload/')
    ela_image= models.ImageField(upload_to='upload/',default="upload/tamp2r.jpg")

    def __str__(self):  
        return str(self.pk)