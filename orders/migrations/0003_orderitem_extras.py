# Generated by Django 2.0.3 on 2018-12-11 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20181211_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='extras',
            field=models.ManyToManyField(to='orders.Extra'),
        ),
    ]
