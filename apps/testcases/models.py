from django.db import models

# Create your models here.


class TestcasesModel(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(verbose_name='用例名称', max_length=50, unique=True, help_text='用例名称')
    interface = models.ForeignKey(to='interfaces.InterfacesModel', on_delete=models.CASCADE, verbose_name='所属接口',
                                  help_text='所属接口', related_name='testcases')
    include = models.TextField(verbose_name='前置', null=True, help_text='用例执行前置顺序')
    author = models.CharField(verbose_name='编写人员', max_length=50, help_text='编写人员')
    request = models.TextField(verbose_name='请求信息', help_text='请求信息')
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否有效', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_testcases'
        verbose_name = '用例信息'
        ordering = ['id']

    def __str__(self):
        return self.name
