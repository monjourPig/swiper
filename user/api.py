from django.core.cache import cache
from lib.http import render_json
from common import error
from user.logic import send_verify_code, check_vcode, save_upload_file
from user.models import User
from user.forms import ProfileForm


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
    key = 'Profile-%s' % user.id
    # 从缓存中获取
    user_profile = cache.get(key)
    # 如果没有就添加
    if not user_profile:
        user_profile = user.profile.to_dict()
        cache.set(key, user_profile)
    return render_json(user_profile)


def modify_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)
    # 检查数据是否正常
    if form.is_valid():
        user = request.user
        # 清洗数据存放
        user.profile.__dict__.update(form.cleaned_data)
        user.profile.save()

        # 修改缓存
        key = 'Profile-%s' % user.id
        cache.set(key, user.profile.to_dict())
        return render_json(None)
    else:
        # 不正常返回错误码
        return render_json(form.errors, error.PROFILE_ERROR)


def upload_avatar(request):
    '''头像上传'''
    # 1.接收用户上传的图像
    # 2.定义用户头像名称
    # 3.异步将图像上传七牛
    # 4.将URL保存入数据库

    file = request.FILES.get('avatar')
    if file:
        save_upload_file(request.user, file)
        return render_json(None)
    else:
        return render_json(None, error.FILE_NOT_FOUND)
