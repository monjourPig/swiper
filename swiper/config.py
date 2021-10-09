'''
第三方平台配置
'''

# 互亿无线短信平台配置

HY_SMS_URL = 'https://106.ihuyi.com/webservice/sms.php?method=Submit'
HY_SMS_PARAMS = {
    'account': 'C06659366',
    'password': '1cc4f78337df4e0b88dd7e6d2d10f2be',
    'content': '您的注册验证码是%s，请不要把验证码泄漏给其他人，如非本人请勿操作。',
    'mobile': None,
    'format': 'json',
}