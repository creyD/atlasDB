# Generated by Django 2.0.2 on 2018-02-20 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atlasUpload', '0006_delete_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='docfile',
            field=models.FileField(upload_to='tasks/%Y/%m'),
        ),
    ]
