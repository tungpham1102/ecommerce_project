# Generated by Django 3.0.3 on 2020-02-17 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='color',
            field=models.CharField(choices=[('R', 'red'), ('B', 'black'), ('W', 'white')], default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], default=0, max_length=3),
            preserve_default=False,
        ),
    ]