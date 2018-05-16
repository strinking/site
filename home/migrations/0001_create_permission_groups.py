# Generated by Django 2.0.3 on 2018-05-16 17:10

from django.contrib.auth.models import Group
from django.db import migrations


def create_guest_group(apps, schema_editor):
    """Create the guest group, to be assigned to non-member users."""

    Group.objects.create(name='guest')


def create_member_group(apps, schema_editor):
    """Create the member group, to be assigned to members."""

    Group.objects.create(name='member')


def create_staff_group(apps, schema_editor):
    """Create the staff group, to be assigned to staff."""

    Group.objects.create(name='staff')


class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0005_remove_guide_editors'),
    ]

    operations = [
        migrations.RunPython(create_guest_group),
        migrations.RunPython(create_member_group),
        migrations.RunPython(create_staff_group)
    ]