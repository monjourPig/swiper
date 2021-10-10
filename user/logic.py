import random

import requests
from swiper import config
from worker import call_by_worker
from django.core.cache import cache


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
