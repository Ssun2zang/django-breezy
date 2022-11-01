from django.db import models

# Create your models here.

class Bridges(models.Model):
    name = models.CharField(max_length=32, verbose_name="교량명")   
    length = models.CharField(max_length=32, verbose_name="교량 길이", default = '') 
    section = models.CharField(max_length=32, verbose_name="section", default = '')
    writer = models.CharField(max_length=32, verbose_name="등록자", default = '')     
    registered_dttm = models.DateTimeField(auto_now_add=True,
                                           verbose_name='등록시간')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'bridges'
        verbose_name = '교량' 
        verbose_name_plural = '교량'
