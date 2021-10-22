import logging

from common import error
from lib.http import render_json

log = logging.getLogger('err')


def perm_require(perm_name):
    '''权限检查装饰器'''

    def deco(view_func):
        def wrap(request):
            user = request.user
            if user.vip.had_perm(perm_name):
                response = view_func(request)
                return response
            else:
                log.error(f'{request.user.nickname} not has{perm_name}')
                return render_json(None, error.NOT_HAS_PERM)

        return wrap

    return deco
