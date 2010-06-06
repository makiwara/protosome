# -*- coding: utf-8 -*-
"""
Этот модуль отвечает за определение хоста и сопоставление ему набор "интересных" данных.
В результате settings обогащается
  * HOSTNAME -- название выбранного варианта
  * HOST -- выбранный вариант из HOSTS, соответствующий HOSTNAME
  * URL -- адрес URL из HOST
  * IS_LOCALHOST, IS_* -- на каждый указанный в HOSTS вариант
  * LOG_FILE -- куда логировать запросы
Хосты можно добавлять сюда -- для удобства реконфигурации, или же класть 
в python path файл host_settings, который содержит ^^^ эти переменные
"""

__all__ = [ "HOSTS", "HOSTNAME", "HOST", "URL", "FORCE_SCRIPT_NAME", "LOG_FILE" ]

# ---- host description
HOSTS = dict(
    localhost = dict( 
        PATH ='.',
        LOG_FILE = None,
        STATIC_ROOT = './static/',
		SECRET = 'wlqejoruteoifgsdhjoruytorweiuo',
        URL = "http://127.0.0.1:8000/" 
	),
)
    
# ---- host detection (insert lines here if needed)
# result -- HOST = corresponding host data
HOSTNAME = "localhost"
HOST = HOSTS[HOSTNAME]
URL = HOST["URL"]
LOG_FILE = HOST["LOG_FILE"]
FORCE_SCRIPT_NAME = ""

# now for IS_LOCALHOST etc. parts
for hostname in HOSTS:
    globals()["IS_%s" % hostname.upper()] = HOSTNAME==hostname
    __all__.append("IS_%s" % hostname.upper())