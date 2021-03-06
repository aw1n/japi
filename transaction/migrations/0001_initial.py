# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-08 03:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('provider', '0001_initial'),
        ('level', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.FloatField(blank=True, null=True)),
                ('withdraw_limit', models.FloatField(blank=True, default=0, null=True)),
                ('bet_sum', models.FloatField(blank=True, null=True)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='balance_member', to='account.Member')),
            ],
        ),
        migrations.CreateModel(
            name='OnlinePayee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('board_url', models.CharField(max_length=255)),
                ('merchant_num', models.CharField(blank=True, max_length=255, null=True)),
                ('certificate', models.CharField(blank=True, max_length=255, null=True)),
                ('merchant_account', models.CharField(blank=True, max_length=255, null=True)),
                ('expired_in', models.IntegerField(blank=True, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('sum_fund', models.FloatField(blank=True, null=True)),
                ('level', models.ManyToManyField(related_name='online_payee_member_level', to='level.Level')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=255, null=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_type', models.IntegerField(blank=True, choices=[(1, 'Normal'), (2, 'Card'), (3, 'Mobile')], default=1, null=True)),
                ('request_parameter', jsonfield.fields.JSONField()),
                ('data_parser', models.IntegerField(blank=True, choices=[(1, 'XML'), (2, 'JSON')], default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemitInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank', models.CharField(blank=True, max_length=255, null=True)),
                ('way', models.CharField(blank=True, max_length=255, null=True)),
                ('depositor', models.CharField(blank=True, max_length=255, null=True)),
                ('deposited_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemitPayee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remit_type', models.IntegerField(blank=True, choices=[(1, 'Normal'), (2, 'Wechat'), (3, 'Alipay')], default=1, null=True)),
                ('payee_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.CharField(blank=True, max_length=255, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('nickname', models.CharField(blank=True, max_length=255, null=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to=b'')),
                ('sum_fund', models.FloatField(blank=True, null=True)),
                ('bank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='remit_payee_bank', to='bank.Bank')),
                ('level', models.ManyToManyField(related_name='remit_payee_member_level', to='level.Level')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(blank=True, choices=[(1, 'Success'), (2, 'Failed'), (3, 'Ongoing'), (4, 'Cancelled')], default=1, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
                ('memo', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_member', to='account.Member')),
                ('online_payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_online_payee', to='transaction.OnlinePayee')),
                ('provider', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_provider', to='provider.Provider')),
                ('remit_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_remit_info', to='transaction.RemitInfo')),
                ('remit_payee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_remit_payee', to='transaction.RemitPayee')),
            ],
            options={
                'db_table': 'transaction',
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_type', to='transaction.TransactionType'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transaction_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='onlinepayee',
            name='payment_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='online_payee_payment_type', to='transaction.PaymentType'),
        ),
    ]
