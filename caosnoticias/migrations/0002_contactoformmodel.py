# Generated by Django 5.0.2 on 2024-07-09 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caosnoticias', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactoFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('ciudad', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
            ],
        ),
    ]