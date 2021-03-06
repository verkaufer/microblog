# Generated by Django 2.0.5 on 2018-05-13 17:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_type', models.IntegerField(choices=[(1, 'Following')])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feed_is_public', models.BooleanField(default=True)),
                ('relations', models.ManyToManyField(related_name='related', through='accounts.Relation', to='accounts.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='relation',
            name='initiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='relation',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='accounts.UserProfile'),
        ),
    ]
