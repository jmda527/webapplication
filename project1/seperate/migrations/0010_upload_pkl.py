# Generated by Django 2.1.5 on 2020-01-21 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seperate', '0009_delete_upload_pkl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload_pkl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.FileField(upload_to='pkl')),
            ],
        ),
    ]