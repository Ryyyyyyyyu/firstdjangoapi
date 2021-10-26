from django.db import models

# Create your models here.


class ProjectsModel(models.Model):
    id = models.IntegerField(verbose_name='项目id', help_text='项目id', primary_key=True)
    name = models.CharField(verbose_name='项目名称', help_text='项目名称', max_length=50)
    leader = models.CharField(verbose_name='项目负责人', help_text='项目负责人', max_length=20)
    tester = models.CharField(verbose_name='测试人员', help_text='项目测试人员', max_length=50)
    programmer = models.CharField(verbose_name='开发人员', help_text='开发人员', max_length=50)
    publish_app = models.CharField(verbose_name='发布应用', help_text='发布应用', max_length=100)
    desc = models.TextField(verbose_name='项目描述', help_text='项目描述', max_length=200, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目表'
        ordering = ['id']

    def __str__(self):
        return self.name
