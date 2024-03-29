'''
Vip - User :一对多
Vip - Permission  : 多对多
'''

from django.db import models


# Create your models here.

class Vip(models.Model):
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField()
    price = models.FloatField()

    def perms(self):
        '''当前VIP具有的所有权限'''
        relations = VipPermRelation.objects.filter(vip_id=self.id)
        perm_id_list = [r.perm_id for r in relations]
        return Permission.objects.filter(id__in=perm_id_list)

    def had_perm(self, perm_name):
        '''检查是否具有某种权限'''
        perm = Permission.objects.get(name=perm_name)
        VipPermRelation.objects.filter(vip_id=self.id, perm_id=perm.id).exists()


class Permission(models.Model):
    '''
    权限表
        vipflag:        会员身份标识
        superlike:      超级喜欢
        rewind:         反悔功能
        anylocation:    任意更改定位
        unlimit_like:   无限喜欢次数
    '''
    name = models.CharField(max_length=32, unique=True)


class VipPermRelation(models.Model):
    '''
    会员套餐-1
        会员身份标识
        超级喜欢

    会员套餐-2
        会员身份标识
        反悔功能
        无限喜欢次数

    会员套餐-3
        会员身份标识
        超级喜欢
        反悔功能
        任意更改定位
        无限喜欢次数
    '''

    vip_id = models.IntegerField()
