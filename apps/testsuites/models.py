from django.db import models

# Create your models here.


class TestsuitsModel(models.Model):
    id = models.AutoField(verbose_name='id主键', primary_key=True, help_text='id主键')
    name = models.CharField(verbose_name='套件名称', max_length=200, unique=True, help_text='套件名称')
    project = models.ForeignKey(to='projects.ProjectsModel', on_delete=models.CASCADE,
                                related_name='testsuits', help_text='所属项目')
    include = models.TextField(verbose_name='包含的接口', null=False, help_text='包含的接口')
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否删除', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_testsuits'
        verbose_name = '套件信息'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name
