# Generated by Django 2.1 on 2018-11-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Input',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perplexity', models.FloatField(default=50, verbose_name='Perplexity')),
            ],
        ),
    ]
