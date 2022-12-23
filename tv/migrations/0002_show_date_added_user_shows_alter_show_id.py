# Generated by Django 4.1.2 on 2022-12-22 02:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tv', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='shows',
            field=models.ManyToManyField(related_name='trackers', to='tv.show'),
        ),
        migrations.AlterField(
            model_name='show',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]