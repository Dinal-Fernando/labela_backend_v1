# Generated by Django 4.0.3 on 2024-01-07 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car_parts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(max_length=40)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_at', models.DateTimeField(auto_now_add=True)),
                ('delivery_date', models.DateField()),
                ('delivery_time', models.TimeField()),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.cart')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_parts.product')),
            ],
        ),
    ]
