# Generated by Django 2.1.5 on 2020-01-19 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seperate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mydb',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='mydb',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
