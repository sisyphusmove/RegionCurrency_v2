# Generated by Django 2.1.2 on 2018-12-04 00:16

from django.db import migrations
import store.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_auto_20181204_0913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=store.fields.ThumbnailImageField(upload_to='store/%store.id/'),
        ),
    ]