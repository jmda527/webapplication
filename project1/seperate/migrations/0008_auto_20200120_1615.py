# Generated by Django 2.1.5 on 2020-01-20 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seperate', '0007_auto_20200120_0214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Upload_pkl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.FileField(upload_to='pkl')),
            ],
        ),
        migrations.DeleteModel(
            name='Upload_excel',
        ),
    ]
