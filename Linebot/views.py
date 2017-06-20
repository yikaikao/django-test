# -*- coding: utf-8 -*-
from django.http import HttpResponse

def here(request):
    return HttpResponse('媽，我在這！')

def add(request, a, b):
    a = int(a)
    b = int(b)
    s = a + b
    d = a - b
    p = a * b
    q = a / b
    html = '<html>sum={s}<br>dif={d}<br>pro={p}<br>quo={q}</html>'.format(s=s,d=d,p=p,q=q)
    return HttpResponse(html)
