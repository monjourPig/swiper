from vip.models import Vip, Permission, VipPermRelation


def init_permission():
    '''创建权限模型'''
    permission_name = [
        'vipflag',  # 会员身份标识
        'superlike',  # 超级喜欢
        'rewind',  # 反悔功能
        'anylocation',  # 任意更改定位
        'unlimit_like',  # 无限喜欢次数
    ]

    for name in permission_name:
        perm, _ = Permission.objects.get_or_create(name=name)
        print('create permission %s' % perm.name)


def init_vip():
    '''创建初始vip等级'''
    for i in range(4):
        vip, _ = Vip.objects.get_or_create(
            name='会员-%d' % i,
            level=i,
            price=i * 5.0
        )
        print('create %s' % vip.name)


def create_vip_perm_relations():
    '''创建Vip 和 Permission的关系'''
    vip1 = Vip.objects.get(level=1)
    vip2 = Vip.objects.get(level=2)
    vip3 = Vip.objects.get(level=3)

    vipflag = Permission.objects.get(name='vipflag')
    superlike = Permission.objects.get(name='superlike')
    rewind = Permission.objects.get(name='rewind')
    anylocation = Permission.objects.get(name='anylocation')
    unlimit_like = Permission.objects.get(name='unlimit_like')

    # 给vip1分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip1.id, perm_id=superlike.id)
    # 给vip2分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id, perm_id=rewind.id)
    # 给vip3分配权限
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=vipflag.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=anylocation.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id, perm_id=unlimit_like.id)


if __name__ == '__main__':
    init_permission()
    init_vip()
    create_vip_perm_relations()
