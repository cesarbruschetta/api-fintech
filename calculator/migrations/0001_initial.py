# Generated by Django 2.0.7 on 2019-05-06 04:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('term', models.PositiveIntegerField()),
                ('rate', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'Loan',
                'verbose_name_plural': 'Loans',
            },
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.CharField(choices=[('missed', 'missed'), ('made', 'made')], max_length=6)),
                ('amount', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('loan', models.ForeignKey(on_delete='PROTECT', to='calculator.Loans')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
