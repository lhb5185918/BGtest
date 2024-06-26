# Generated by Django 5.0.5 on 2024-05-21 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_alter_userinfo_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricePolicy',
            fields=[
                ('price_id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.SmallIntegerField(choices=[(1, '免费版'), (2, '收费版'), (3, '其他')], default=2, verbose_name='收费类型')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('price', models.PositiveIntegerField(verbose_name='价格')),
                ('project_num', models.PositiveIntegerField(verbose_name='项目数')),
                ('project_member', models.PositiveIntegerField(verbose_name='项目成员数')),
                ('project_space', models.PositiveIntegerField(verbose_name='项目空间')),
                ('per_file_size', models.PositiveIntegerField(verbose_name='单文件大小')),
                ('creat_datatime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名')),
                ('color', models.CharField(choices=[('1', '#56b8eb'), ('2', '#f28033'), ('3', '#ebc656'), ('4', '#a2d148'), ('5', '#20BFA4'), ('6', '#7461c2'), ('7', '#20BFA3'), ('8', '#ebc656')], default=1, max_length=32, verbose_name='颜色')),
                ('user_space', models.IntegerField(default=0, verbose_name='项目空间')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='项目描述')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('join_count', models.IntegerField(default=1, verbose_name='参与人数')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='web.userinfo', verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.project', verbose_name='项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='参与者')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(1, '未支付'), (2, '已支付')], verbose_name='状态')),
                ('order', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
                ('count', models.IntegerField(help_text='0表示无限期', verbose_name='数量（年）')),
                ('price', models.IntegerField(verbose_name='实际支付价格')),
                ('start_datetime', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_datetime', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('create_datetime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('price_policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.pricepolicy', verbose_name='价格策略')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.userinfo', verbose_name='用户')),
            ],
        ),
    ]
