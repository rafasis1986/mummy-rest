# Generated by Django 2.1.7 on 2019-03-12 19:49

from django.db import migrations, models
import mummyrest.apps.members.models


def insert_mummy_user(apps, schema):
    _Member = apps.get_model('members', 'Member')

    mummy, _ = _Member.objects.get_or_create(id=1)
    mummy.is_staff = True
    mummy.is_superuser = True
    mummy.depth = 0
    mummy.parent = 0
    mummy.start_week = 0
    mummy.set_password('mummy')
    mummy.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('password', models.CharField(default='money', max_length=128)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('depth', models.PositiveIntegerField(default=0)),
                ('parent', models.BigIntegerField()),
                ('channel', models.CharField(max_length=128)),
                ('mummy_money', models.FloatField(default=0)),
                ('start_week', models.PositiveIntegerField(default=0)),
                ('map_tree', models.TextField(blank=True)),
                ('innocence', models.FloatField(default=0)),
                ('experience', models.FloatField(default=0)),
                ('charisma', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'member',
                'abstract': False,
            },
            managers=[
                ('objects', mummyrest.apps.members.models.MembersManager()),
            ],
        ),
        migrations.RunPython(insert_mummy_user)
    ]