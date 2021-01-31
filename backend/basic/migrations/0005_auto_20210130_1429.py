# Generated by Django 3.1.4 on 2021-01-30 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_auto_20210124_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlocation',
            name='capacity_indoor_corona',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='eventlocation',
            name='capacity_outdoor_corona',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='participantgroup',
            name='participant_role',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='basic.role'),
        ),
        migrations.AddField(
            model_name='participantpersonal',
            name='participant_role',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='basic.role'),
        ),
        migrations.DeleteModel(
            name='ParticipantRole',
        ),
    ]