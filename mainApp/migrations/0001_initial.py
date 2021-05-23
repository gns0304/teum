# Generated by Django 3.2.2 on 2021-05-23 04:33

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
            name='Complexity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(choices=[(1, '평일'), (2, '토요일'), (3, '일요일')], verbose_name='요일')),
            ],
            options={
                'verbose_name': '혼잡도 정보',
                'verbose_name_plural': '혼잡도 정보 관리',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line', models.CharField(max_length=6, verbose_name='호선')),
                ('name', models.CharField(max_length=10, verbose_name='역명')),
                ('foothold', models.BooleanField(default=False, verbose_name='발판 유무')),
                ('platform', models.PositiveSmallIntegerField(choices=[(1, '상행선'), (2, '하행선')], verbose_name='승강장번호')),
            ],
            options={
                'verbose_name': '역 정보',
                'verbose_name_plural': '역 정보 관리',
            },
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, verbose_name='시간')),
                ('complexity', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='혼잡도')),
                ('complex_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.complexity', verbose_name='혼잡도 정보')),
            ],
            options={
                'verbose_name': '혼잡도 시간정보',
                'verbose_name_plural': '혼잡도 시간정보 관리',
            },
        ),
        migrations.CreateModel(
            name='FavoriteStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.station', verbose_name='즐겨 찾는 역')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='계정 정보')),
            ],
            options={
                'verbose_name': '즐겨 찾는 역 정보',
                'verbose_name_plural': '즐겨 찾는 역 정보 관리',
            },
        ),
        migrations.CreateModel(
            name='Door',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_number', models.PositiveSmallIntegerField(verbose_name='차량순서')),
                ('door_number', models.PositiveSmallIntegerField(verbose_name='차량출입문번호')),
                ('distance', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='안전거리')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.station', verbose_name='역 정보')),
            ],
            options={
                'verbose_name': '안전거리 정보',
                'verbose_name_plural': '안전거리 정보 관리',
            },
        ),
        migrations.AddField(
            model_name='complexity',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.station', verbose_name='역 정보'),
        ),
    ]
