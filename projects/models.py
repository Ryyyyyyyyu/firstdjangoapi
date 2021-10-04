from django.db import models

# Create your models here.


class ProjectsModel(models.Model):
    id = models.IntegerField(verbose_name='项目id', help_text='项目id', primary_key=True)
    name = models.CharField(verbose_name='项目名称', help_text='项目名称', max_length=50)
    leader = models.CharField(verbose_name='项目负责人', help_text='项目负责人', max_length=20)
    desc = models.TextField(verbose_name='项目描述', help_text='项目描述', max_length=200, null=True, blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目表'
        ordering = ['id']

    def __str__(self):
        return self.name
