# Generated by Django 3.2.9 on 2022-05-30 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torebki', '0002_alter_priceshistory_price_from'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='paper_type',
            field=models.CharField(choices=[('powlekany', 'powlekany'), ('niepowlekany', 'niepowlekany')], default='niepowlekany', max_length=100),
        ),
    ]
