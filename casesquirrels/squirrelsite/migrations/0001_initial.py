# Generated by Django 3.1.3 on 2021-01-01 01:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Puzzle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.CharField(max_length=200)),
                ('initial_points', models.IntegerField()),
                ('live_date', models.DateTimeField(verbose_name='Puzzle Activation Date')),
                ('times_solved', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('phase', models.IntegerField(choices=[(1, 'Day 1'), (2, 'Day 2'), (3, 'Day 3'), (4, 'Day 4'), (5, 'Day 5')])),
                ('type', models.CharField(choices=[('WB', 'Web-Based'), ('IB', 'Image-Based'), ('SM', 'Secret Message')], max_length=2)),
                ('difficulty', models.IntegerField(choices=[(0, 'Easy'), (1, 'Moderate'), (2, 'Difficult'), (3, 'Near-Impossible'), (4, 'Easter Egg')])),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6)),
                ('image', models.ImageField(upload_to='inventory')),
                ('puzzle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='squirrelsite.puzzle')),
            ],
        ),
    ]