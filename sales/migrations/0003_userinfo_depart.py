# Generated by Django 3.2 on 2021-06-04 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_campuses_classlist_customer_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.department'),
        ),
    ]
