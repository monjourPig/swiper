import datetime

from django.db import models
from django.utils.functional import cached_property
from lib.orm import ModelMixin


# Create your models here.
class User(models.Model):
    '''用户数据模型'''
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )

    nickname = models.CharField(max_length=32, unique=True)
    phonenum = models.CharField(max_length=16, unique=True)
    sex = models.CharField(max_length=8, choices=SEX)
    birth_year = models.IntegerField(default=2000)
    birth_month = models.IntegerField(default=1)
    birth_day = models.IntegerField(default=1)
    avatar = models.CharField(max_length=256)  # 头像
    location = models.CharField(max_length=32)

    @cached_property
    def age(self):
        today = datetime.date.today()
        birth_data = datetime.date(self.birth_year, self.birth_month, self.birth_day)

        x = (today - birth_data).days // 365
        return x

    # 构建user表与用户设置表的关系
    @property
    def profile(self):
        # 对象本身所有的属性都保存在self.__dict__中;      hasattr(self, 属性)，判断这个对象有没有某个属性
        if not hasattr(self, '_profile'):
            self._profile, _ = Profile.objects.get_or_create(id=self.id)
        return self._profile

    # 将user对象转换成dict类型，方便将其转换成json传输
    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'phonenum': self.phonenum,
            'sex': self.sex,
            'avatar': self.avatar,
            'location': self.location,
            'age': self.age,
        }


# 用户设置类
class Profile(models.Model, ModelMixin):
    ''' 用户配置项 '''
    SEX = (
        ('男', '男'),
        ('女', '女'),
    )

    location = models.CharField(default='中国', max_length=32, verbose_name='目标城市')

    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=45, verbose_name='最大交友年龄')

    dating_sex = models.CharField(default='女', max_length=8, choices=SEX, verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='是否开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='是否自动播放视频')
