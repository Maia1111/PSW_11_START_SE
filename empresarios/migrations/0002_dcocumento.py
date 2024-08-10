# Generated by Django 5.0.8 on 2024-08-10 14:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dcocumento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('arquivo', models.FileField(upload_to='documentos')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresarios.empresas')),
            ],
        ),
    ]
