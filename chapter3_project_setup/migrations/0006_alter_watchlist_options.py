# Generated by Django 4.2.3 on 2024-10-20 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chapter3_project_setup', '0005_alter_watchlist_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='watchlist',
            options={'permissions': (('can_view_watchlist', 'User can view watchlist'), ('can_create_watchlist', 'User can create watchlist'), ('can_update_watchlist', 'User can update watchlist'), ('can_partially_update_watchlist', 'User can partially update watchlist'), ('can_delete_watchlist', 'User can delete watchlist')), 'verbose_name': 'Watch List', 'verbose_name_plural': 'Watchlists'},
        ),
    ]
