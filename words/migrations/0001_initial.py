# Generated by Django 2.0.3 on 2018-08-11 10:45

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
            name='example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='meaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meaning', models.TextField()),
                ('syn', models.CharField(blank=True, max_length=30, null=True)),
                ('opp', models.CharField(blank=True, max_length=30, null=True)),
                ('examples', models.ManyToManyField(blank=True, to='words.example')),
            ],
        ),
        migrations.CreateModel(
            name='word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spell', models.CharField(max_length=30)),
                ('mood', models.CharField(max_length=10)),
                ('note', models.CharField(blank=True, max_length=30, null=True)),
                ('slug', models.CharField(max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('meanings', models.ManyToManyField(blank=True, to='words.meaning')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='meaning',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.word'),
        ),
        migrations.AddField(
            model_name='example',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='words.meaning'),
        ),
    ]
