# Generated by Django 2.1.1 on 2018-09-20 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20180918_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('N', 'Not Chosen'), ('M', 'Male'), ('F', 'Female')], default='N', max_length=1),
        ),
    ]
