# Generated by Django 4.1.6 on 2023-04-20 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_userprofile_cover_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cover_pic',
            field=models.ImageField(blank=True, default='/profilepics/abcd.jpg', upload_to='images/cover_pic'),
        ),
    ]
