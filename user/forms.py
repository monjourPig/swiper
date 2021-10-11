from django import forms
from user.models import Profile


class ProfileForm(forms.ModelForm):
    '''处理用户个人资料类'''
    # 具体指向某一个model
    class Meta:
        model = Profile
        fields = [
            'dating_sex',
            'location',
            'min_distance',
            'max_distance',
            'min_dating_age',
            'max_dating_age',
            'vibration',
            'only_matche',
            'auto_play',
        ]


        # 清洗数据
        def clean_max_dating_age(self):
            cleaned_data = super().clean()
            min_dating_age = cleaned_data.get('min_dating_age')
            max_dating_age = cleaned_data.get('max_dating_age')
            # 判断最小年龄是否大于最大年龄
            if min_dating_age > max_dating_age:
                # 注意，这个函数执行时如果抛出异常，不会接着匹配下面的字段
                raise forms.ValidationError('min_dating_age > max_dating_age')


