import random
import os
import requests

from urllib.parse import urljoin
from django.conf import settings
from swiper import config
from worker import call_by_worker
from django.core.cache import cache
from lib.qncloud import async_upload_to_qiniu



def gen_verify_code(length=6):
    '''产生一个验证码'''
    return random.randrange(10 ** (length - 1), 10 ** length)


@call_by_worker
def send_verify_code(phonenum):
    # 异步celery发送验证码
    # 获取一个6位数验证码
    vcode = gen_verify_code()
    # 将验证码保存在django缓存中，实现60秒过期功能
    key = 'VerifyCode-%s' % phonenum
    cache.set(key, vcode, 60)  # 传入一个字典
    # 获取一个浅拷贝HY_SNS_PARAMS
    sms_cfg = config.HY_SMS_PARAMS.copy()
    sms_cfg['content'] = sms_cfg['content'] % vcode
    sms_cfg['mobile'] = phonenum
    response = requests.post(config.HY_SMS_URL, data=sms_cfg)
    return response


def check_vcode(phonenum, vcode):
    '''检查验证码'''
    key = 'VerifyCode-%s' % phonenum
    # 将存放在cache中的vcode取出做验证
    saved_vcode = cache.get(key)
    return saved_vcode == vcode


def save_upload_file(user, upload_file):
    # 1.接收用户上传的图像
    # 2.定义用户头像名称
    ext_name = os.path.splitext(upload_file.name)[-1]
    filename = 'Avatar-%s%s' % (uid, ext_name)
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    with open(filepath, 'wb') as newfile:
        for chunk in upload_file.chunks():
            newfile.write(chunk)
    # 3.异步将图像上传七牛
    async_upload_to_qiniu(filepath, filename)
    # 4.将URL保存入数据库
    url = urljoin(config.QN_BASE_URL, filename)     # 用urllib.parse库中的urljoin方法拼成url
    user.avatar = url
    user.save()
