# Generated by Django 3.1.3 on 2022-10-18 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='customer',
            field=models.CharField(default='공공', max_length=5),
        ),
    ]
