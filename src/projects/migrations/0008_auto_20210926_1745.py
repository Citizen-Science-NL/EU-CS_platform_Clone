# Generated by Django 2.2.13 on 2021-09-26 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20210926_1722'),
    ]

    operations = [
        migrations.RenameField(
            model_name='translatedproject',
            old_name='translatedequipment',
            new_name='translatedEquipment',
        ),
    ]
