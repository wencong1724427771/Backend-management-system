# Generated by Django 3.2 on 2021-06-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_userinfo_depart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campuses',
            options={'verbose_name': '校区表', 'verbose_name_plural': '校区表'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='deal_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
