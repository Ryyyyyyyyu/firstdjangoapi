from django.db import models


# Create your models here.


class DebugtalksModel(models.Model):
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='debugtalk文件名称', help_text='debugtalk文件名称', max_length=200,
                            default='debugtalk.py')
    debugtalk = models.TextField(verbose_name='debugtalk.py文件', help_text='debugtalk.py文件', null=True,
                                 default='#debugtalk.py')
    project = models.OneToOneField(to='projects.ProjectsModel', on_delete=models.CASCADE,
                                   related_name='debugtalks', help_text='所属项目')
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否有效', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_debugtalks'
        verbose_name = 'debugtalk.py文件'
        ordering = ['id']

    def __str__(self):
        return self.name
