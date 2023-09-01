# Generated by Django 4.2.4 on 2023-09-01 11:16

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_address_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'txt', 'text', 'xls', 'xlsx'])])),
                ('file_version', models.CharField(max_length=20)),
                ('uploadtime', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='useruploads',
            name='file',
        ),
        migrations.RemoveField(
            model_name='useruploads',
            name='uploadtime',
        ),
        migrations.AddField(
            model_name='useruploads',
            name='file_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='useruploads',
            name='files',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.files'),
            preserve_default=False,
        ),
    ]