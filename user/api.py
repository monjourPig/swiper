from lib.http import render_json
from common import error
from user.logic import send_verify_code, check_vcode
from user.models import User


# Create your views here.


def get_verify_code(request):
    '''手机注册'''
    phonenum = request.GET.get('phonenum')
    send_verify_code(phonenum)
    return render_json(None, 0)


def login(request):
    '''短信验证登录'''
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    if check_vcode(phonenum, vcode):
        # 获取用户,如果没有就创建。完成注册或登录时直接创建用户过程
        user, created = User.objects.get_or_create(phonenum=phonenum)

        # 记录用户登录状态
        request.session['uid'] = user.id
        return render_json(user.to_dict())
    else:
        return render_json(None, error.VCODE_ERROR)


def get_profile(request):
    '''获取个人资料'''
    user = request.user
    return render_json(user.profile.to_dict())


def modify_profile(request):
    '''修改个人资料'''
    pass


def upload_avatar(request):
    '''头像上传'''
    pass
