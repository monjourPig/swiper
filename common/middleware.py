from django.utils.deprecation import MiddlewareMixin
from user.models import User
from lib.http import render_json
from common import error


class AuthMiddleware(MiddlewareMixin):
    '''用户登录验证中间件'''

    # 添加白名单
    WHITE_LIST = [
        'api/user/verify',
        'api/user/login'
    ]

    def process_request(self, request):
        # 如果请求的URL在白名单内，直接跳过检查
        for path in self.WHITE_LIST:
            if request.path.startswith(path):
                return

        # 进行登录检查：
        # 从请求的session中获取uid，
        uid = request.session.get('uid')
        if uid:
            try:
                # 如果用户已登录，创建USER对象
                request.user = User.objects.get(id=uid)
                return
            except User.DoesNotExist:
                # 如果用户不存在，刷新下session
                request.session.flush()
        # 如果session中没有uid，则返回一个错误码LOGIN_ERROR,交给前端处理
        return render_json(None, code=error.LOGIN_ERROR)
