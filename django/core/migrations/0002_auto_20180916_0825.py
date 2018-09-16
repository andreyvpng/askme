# Generated by Django 2.1.1 on 2018-09-16 08:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='core.Answer')),
                ('liked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_related_name': 'likes',
            },
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('answer', 'liked_by')},
        ),
    ]