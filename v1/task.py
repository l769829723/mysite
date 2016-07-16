from __future__ import absolute_import

from celery import shared_task
import time


@shared_task
def add(x, y):
    print('*** arg: %d + arg: %d ***' % (x, y))
    time.sleep(10)
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)