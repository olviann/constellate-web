# Generated by Django 4.2.2 on 2023-06-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_client_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='icon',
            field=models.FileField(upload_to='C:/Users/ovycl/constellate/constellatebackend/'),
        ),
    ]