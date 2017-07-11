#!/usr/bin/env python
# coding: utf-8
from imp import reload
import os
import sys
import imp
# 将系统的编码设置为UTF8
imp.reload(sys)
#sys.setdefaultencoding('utf-8')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")

#from django.core.handlers.wsgi import WSGIHandler
#application = WSGIHandler()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()