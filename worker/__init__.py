import os
from celery import Celery

# 设置环境变量，加载Django的settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiper.settings')

# 创建Celery Application
celery_app = Celery('swiper')
# 从worker.config加载配置
celery_app.config_from_object('worker.config')

celery_app.autodiscover_tasks()


# 创建一个召唤worker的函数
def call_by_worker(func):
    '''将任务在Celery中异步执行'''
    task = celery_app.task(func)
    return task.delay
