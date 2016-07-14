# -*- coding:utf8 -*-

import time
from celery.task import task

@task
def _my_background_task(name):
    for i in range (1, 10):
        print('Hello DjCelery! -> %s, %s' % (name, i))
        time.sleep(1)