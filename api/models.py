from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)




class UserUploads(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    file_type = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/', validators=[FileExtensionValidator(allowed_extensions=['pdf','txt','text','xls', 'xlsx'])])
    uploadtime = models.DateField(auto_now_add=True)



class Address(models.Model):
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    first_address = models.CharField(max_length=255)
    second_address = models.CharField(max_length=255,null=True)
    landmark = models.CharField(max_length=255,null= True)
    city = models.CharField(max_length=255)
    pin_code = models.IntegerField(null=True)
    contact_no = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)