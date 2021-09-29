from django.db import models
from django.contrib.auth.models import User

import uuid
from .validators import validate_file_extension

# Create your models here.
class MetaData(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    file= models.FileField(upload_to='files/', validators=[validate_file_extension])
    file_details =models.TextField()
    uu_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
   
