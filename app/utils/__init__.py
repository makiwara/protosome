# -*- coding: utf-8 -*-
"""
В этом модуле лежат декораторы и прочие утилитки.

Кроме более-менее внятных, есть набор функций сомнительного качества:
  * is_email(what)
  * is_http(what)
  * new_url(cls, field="url", prefix="", min_len=5) -- создает уникальный в рамках класса короткий урл
"""
import re
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe


# Разные утилиты сомнительного качества

def is_email(what):
    """ Проверка, является ли строка емайл-адресом (очень простая) """
    return re.match( r'^[a-z0-9.\-_]+@[a-z0-9.\-]+\.[a-z]{2,4}', what, re.I )

def is_http(what):
    """ Проверка, является ли строка http-адресом (очень простая) """
    return re.match( r'^http://[a-z0-9.\-]+\.[a-z]{2,4}(.*)', what, re.I )
    

    
def new_url(cls, field="url", prefix="", min_len=5):
    """ Генерация нового уникального урла """
    prefix = re.sub(r'[^0-9a-zA-Z_-]+','',re.sub(r'@.*$', '', prefix )).strip()
    t = User.objects.make_random_password(30)
    if prefix == "":
        c = min_len
    else:
        c = 0
    while True:
        try:
            u = cls.objects.get(**{field:prefix+t[:c]})
            c = c+1
            if c >= len(t):
                t = User.objects.make_random_password(30)
        except:
            return prefix+t[:c]
    
    
