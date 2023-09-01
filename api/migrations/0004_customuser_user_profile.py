# Generated by Django 4.2.4 on 2023-09-01 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_address_landmark_alter_address_pin_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='User_profile',
            field=models.ImageField(default='', upload_to='user_profile/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png'])]),
            preserve_default=False,
        ),
    ]
