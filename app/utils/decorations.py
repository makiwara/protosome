# -*- coding: utf-8 -*-
"""
Этот модуль содержит полезные декораторы, которые облегчают жизнь при типовой обработке запросов:

  @require_auth
  @require_not_auth

  @return_json
  def something(request, **etc):
      return dict(....)

И несколько функций, которые я пока боюсь превращать в декораторы тоже:

  not_found() -- возвращает рендеринг 404 страницы.
  
  tpl( template, ctx, request=None ) -- Render to response, по дороге насыщает context полезными ништяками:
    - request = UserRequestContext
    - settings = django settings
  tpls( template, ctx, request=None ) -- Render to string с теми же свойствами
  
Отсюда же можно доставать полезняшку mark_safe -- никогда не могу запомнить, где она лежит.
  
NB: UserRequestContext поставляется в registration app, но если такой нет, то берется просто RequestContext из django.template
"""
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response as _tpl
from django.template.loader import render_to_string as _tpls
from django.conf import settings
from django.utils import simplejson
from django.core.mail import mail_admins
from django.utils.translation import ugettext as _
from django.contrib.auth import logout as django_logout
import sys

try:
    from registration.models import UserRequestContext, Person
except:
    from django.template import RequestContext as UserRequestContext
    class Person:
        @classmethod 
        def From(cls, what):
            return True


def tpl_ctx(ctx=None, req=None):
    if ctx is None: ctx=dict()
    if req is not None:
        ctx["request"] = UserRequestContext(req)
    ctx["test"]=1
    ctx["settings"] = settings
    return ctx

def tpl(tplt, ctx=None, request=None):
    return _tpl( tplt, tpl_ctx(ctx, request) )
    
def tpls(tplt, ctx=None, request=None):
    return _tpls( tplt, tpl_ctx(ctx, request) )
    
def not_found():
    return tpl('404.html')

def require_auth(func):
    """ Требование авторизации пользователя для работы данного view """
    def auth_handle(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/")
        else:
            if Person.From(request.user) is None:
                django_logout(request)
                return HttpResponseRedirect("/")
            else:
                return func( request, *args, **kwargs)
    return auth_handle


def require_not_auth(func):
    """ Требование, чтобы пользователь был не авторизован """
    def auth_handle(request, *args, **kwargs):
        if request.user.is_authenticated() and Person.From(request.user) is not None:
            return HttpResponseRedirect('/me')
        else:
            return func( request, *args, **kwargs)
    return auth_handle
    
    
def return_json(func):
    """ 
    Декоратор для возврата json-a 
    http://www.djangosnippets.org/snippets/622/
    """
    def wrap(request, *a, **kw):
        response = None
        try:
            try:
                response = dict(func(request, *a, **kw))
            except Exception, e:
                exc_info = sys.exc_info()
                import traceback
                response = dict(result='error', exception=str(e), trace=traceback.format_exception(*exc_info))
            if 'result' not in response:
                response['result'] = 'ok'
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception, e:
            # Mail the admins with the error
            exc_info = sys.exc_info()
            subject = 'JSON view error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = 'Request repr() unavailable'
            import traceback
            message = 'Traceback:\n%s\n\nRequest:\n%s' % (
                '\n'.join(traceback.format_exception(*exc_info)),
                request_repr,
                )
            print message
            mail_admins(subject, message, fail_silently=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
            else:
                msg = _('Internal error')+': '+str(e)
            response = {'result': 'error',
                        'text': message}
                        #'text': msg}
        json = simplejson.dumps(response)
        return HttpResponse(json, mimetype='application/json')
    return wrap