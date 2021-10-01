from django.db import models


# Create your models here.


class InterfacesModel(models.Model):
    id = models.IntegerField(verbose_name='接口id', help_text='接口id', primary_key=True)
    name = models.CharField(verbose_name='接口名称', help_text='接口名称', max_length=50)
    tester = models.CharField(verbose_name='测试人员', help_text='测试人员', max_length=20)
    desc = models.TextField(verbose_name='接口描述', help_text='接口描述', max_length=200, null=True, blank=True)

    project = models.ForeignKey('projects.ProjectsModel', on_delete=models.CASCADE, verbose_name='接口所属项目',
                                help_text='接口所属项目')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_interfaces'
        verbose_name = '接口表'
        ordering = ['id']

    def __str__(self):
        return self.name
