# Generated by Django 3.2.6 on 2021-08-31 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0005_permission_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='url_name',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
