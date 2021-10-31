from django.db import models

# Create your models here.


class ReportsModel(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField('报告名称', max_length=200, unique=True, help_text='报告名称')
    result = models.BooleanField('执行结果', default=True, help_text='执行结果')   # 1为成功, 0为失败
    count = models.IntegerField('用例总数', help_text='总用例数')
    success = models.IntegerField('成功总数', help_text='成功总数')
    html = models.TextField('报告HTML源码', help_text='报告HTML源码', null=True, blank=True, default='')
    summary = models.TextField('报告详情', help_text='报告详情', null=True, blank=True, default='')
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否有效', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_reports'
        verbose_name = '测试报告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
