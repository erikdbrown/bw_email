# Generated by Django 3.1.7 on 2021-03-06 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('to_email', models.TextField()),
                ('to_name', models.TextField()),
                ('from_email', models.TextField()),
                ('from_name', models.TextField()),
                ('subject', models.TextField()),
                ('body', models.TextField()),
                ('external_id', models.TextField()),
                ('provider', models.TextField(choices=[('spendgrid', 'spendgrid'), ('snailgun', 'snailgun')])),
            ],
        ),
    ]