# Generated by Django 3.0.4 on 2020-04-10 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbmsapp', '0004_doctorschedule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='doctorschedule',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dbmsapp.Doctor', to_field='name'),
        ),
    ]
