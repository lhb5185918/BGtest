from django.db import models

# Create your models here.


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, verbose_name='用户名')
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
