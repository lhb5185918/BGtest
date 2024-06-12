from django.db import models

# Create your models here.


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名', db_index=True)  # dc_index=True表示为该字段创建索引
    password = models.CharField(max_length=32, verbose_name='密码')
    email = models.CharField(max_length=32, verbose_name='邮箱')
    phone = models.CharField(max_length=32, verbose_name='电话')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'BG_user_info'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name
        ordering = ['user_id']


class PricePolicy(models.Model):  # 价格策略
    category_choice = ((1, '免费版'), (2, '收费版'), (3, '其他'))
    price_id = models.AutoField(primary_key=True)
    category = models.SmallIntegerField(choices=category_choice, verbose_name='收费类型', default=2)
    # @SmallIntegerField表示小整数
    title = models.CharField(max_length=32, verbose_name='标题')
    price = models.PositiveIntegerField(verbose_name='价格')  # @PositiveIntegerField表示正整数

    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小')

    creat_datatime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Transaction(models.Model):  # 交易记录
    status_choice = ((1, '未支付'), (2, '已支付'))

    status = models.SmallIntegerField(choices=status_choice, verbose_name='状态')
    order = models.CharField(max_length=64, unique=True, verbose_name='订单号')  # @unique=True表示唯一 唯一索引，查询速度较快
    user = models.ForeignKey(to='UserInfo', verbose_name='用户', on_delete=models.CASCADE)  # @ForeignKey表示外键
    price_policy = models.ForeignKey(to='PricePolicy', verbose_name='价格策略', on_delete=models.CASCADE)  # @ForeignKey表示外键
    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')
    price = models.IntegerField(verbose_name='实际支付价格')
    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Project(models.Model):  # 项目表
    color_choice = (('1', '#56b8eb'),
                    ('2', '#f28033'),
                    ('3', '#ebc656'),
                    ('4', '#a2d148'),
                    ('5', '#20BFA4'),
                    ('6', '#7461c2'),
                    ('7', '#20BFA3'),
                    ('8', '#ebc656'))
    name = models.CharField(max_length=32, verbose_name='项目名')
    color = models.CharField(max_length=32, verbose_name='颜色', choices=color_choice, default=1)
    # @color_choice表示颜色选择
    user_space = models.IntegerField(verbose_name='项目空间',default=0)
    desc = models.TextField(verbose_name='项目描述', null=True, blank=True)  # @null=True表示可以为空 @blank=True表示可以为空字符串
    star = models.BooleanField(default=False, verbose_name='星标')
    join_count = models.IntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(to='UserInfo', verbose_name='创建者', related_name='creator', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class ProjectUser(models.Model):  # 项目参与者
    project = models.ForeignKey(to='Project', verbose_name='项目', on_delete=models.CASCADE)
    user = models.ForeignKey(to='UserInfo', verbose_name='参与者', on_delete=models.CASCADE)  # @related_name表示反向查询名
    star = models.BooleanField(default=False, verbose_name='星标')
    # invitee = models.ForeignKey(to='UserInfo', verbose_name='邀请者', related_name='invitee')  # @related_name表示反向查询名
    create_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')


class Wiki(models.Model):
    project = models.ForeignKey(to='Project', verbose_name='项目', on_delete=models.CASCADE)
    title = models.CharField(max_length=32, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    parent = models.ForeignKey(to='Wiki', verbose_name='父文章', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    depth = models.IntegerField(verbose_name='深度', default=1)   # @depth表示深度,默认为1，对应一级标题

    def __str__(self):
        return self.title