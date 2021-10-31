from django.db import models


# Create your models here.


class ConfiguresModel(models.Model):
    id = models.AutoField(verbose_name='配置id', help_text='配置id', primary_key=True)
    name = models.CharField(verbose_name='配置名称', help_text='配置名称', max_length=50)
    interface = models.ForeignKey(to='interfaces.InterfacesModel', on_delete=models.CASCADE, verbose_name='配置所属接口',
                                  help_text='配置所属接口', related_name='configures')
    author = models.CharField(verbose_name='编写人员', help_text='编写人员', max_length=50)
    request = models.TextField(verbose_name='请求信息', help_text='请求信息')
    is_valid = models.BooleanField(verbose_name='是否有效', help_text='是否有效', default=True)
    is_delete = models.BooleanField(verbose_name='是否删除', help_text='是否删除', default=False)
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='创建时间', auto_now=True)

    class Meta:
        db_table = 'tb_configures'
        verbose_name = '配置信息表'
        ordering = ['id']

    def __str__(self):
        return self.name
