# Generated by Django 2.1.4 on 2019-01-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operate', '0004_chartstat_tx_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chartstat',
            name='tx_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]