# Generated by Django 4.0.4 on 2022-04-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('grammage', models.CharField(max_length=5)),
                ('paper_type', models.CharField(choices=[('coated', 'coated'), ('uncoated', 'uncoated')], default='uncoated', max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]