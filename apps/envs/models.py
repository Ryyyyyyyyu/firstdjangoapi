from django.db import models

# Create your models here.


class EnvsModel(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(verbose_name='环境名称', max_length=200, unique=True, help_text='环境名称')
    base_url = models.URLField(verbose_name='请求base url', max_length=200, help_text='请求base url')
    desc = models.TextField(verbose_name='简要描述', help_text='简要描述', max_length=200, null=True, blank=True)
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否有效', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_envs'
        verbose_name = '环境信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
